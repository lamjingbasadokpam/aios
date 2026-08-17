"""Controlled access boundary for the Memory Fabric."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime
from typing import Any
from uuid import UUID

from .contracts import MemoryQuery, MemoryRecord, MemoryScope, MemoryType
from .retriever import MemoryRetriever
from .store import MemoryStore


class MemoryAccessDenied(PermissionError):
    """Raised when a caller attempts to cross its authorized memory boundary."""


@dataclass(frozen=True, slots=True)
class MemoryAccessContext:
    """Immutable authorization context created by a trusted execution boundary."""

    agent_id: UUID | None = None
    session_id: UUID | None = None
    user_id: UUID | None = None
    task_id: UUID | None = None
    allowed_scopes: frozenset[MemoryScope] = frozenset({MemoryScope.AGENT})

    def identity_for(self, scope: MemoryScope) -> UUID | None:
        return {
            MemoryScope.SYSTEM: None,
            MemoryScope.AGENT: self.agent_id,
            MemoryScope.SESSION: self.session_id,
            MemoryScope.USER: self.user_id,
            MemoryScope.TASK: self.task_id,
        }[scope]


class MemoryGateway:
    """Policy boundary between trusted execution context and memory providers."""

    def __init__(self, store: MemoryStore, retriever: MemoryRetriever | None = None) -> None:
        self._store = store
        self._retriever = retriever or MemoryRetriever(store)

    @staticmethod
    def _check_scope(context: MemoryAccessContext, scope: MemoryScope) -> None:
        if scope not in context.allowed_scopes:
            raise MemoryAccessDenied(f"Memory scope '{scope.value}' is not authorized")
        if scope is not MemoryScope.SYSTEM and context.identity_for(scope) is None:
            raise MemoryAccessDenied(f"No caller identity is available for memory scope '{scope.value}'")

    @classmethod
    def _check_record_access(cls, context: MemoryAccessContext, record: MemoryRecord) -> None:
        cls._check_scope(context, record.scope)
        if record.scope is not MemoryScope.SYSTEM and record.owner_id != context.identity_for(record.scope):
            raise MemoryAccessDenied(f"Memory '{record.memory_id}' is not owned by the caller")

    @staticmethod
    def _validate_namespace(namespace: str) -> None:
        if not namespace or namespace.strip() != namespace:
            raise ValueError("Memory namespace must be non-empty and have no surrounding whitespace")

    def remember(self, content: str, *, source: str, context: MemoryAccessContext, namespace: str = "default",
                 metadata: dict[str, Any] | None = None, memory_type: MemoryType = MemoryType.SEMANTIC,
                 scope: MemoryScope = MemoryScope.AGENT, expires_at: datetime | None = None,
                 supersedes_id: UUID | None = None) -> MemoryRecord:
        self._check_scope(context, scope)
        self._validate_namespace(namespace)
        owner_id = context.identity_for(scope)
        if supersedes_id is not None:
            current = next((r for r in self._store.list(namespace) if r.memory_id == supersedes_id), None)
            if current is None:
                raise KeyError(f"Unknown memory: {supersedes_id}")
            self._check_record_access(context, current)
        return self._store.remember(content, source=source, namespace=namespace, metadata=metadata,
                                    memory_type=memory_type, scope=scope, owner_id=owner_id,
                                    expires_at=expires_at, supersedes_id=supersedes_id)

    def recall(self, query: MemoryQuery, *, context: MemoryAccessContext) -> list:
        scope = query.scope or MemoryScope.AGENT
        self._check_scope(context, scope)
        self._validate_namespace(query.namespace)
        if query.scope is None:
            query = replace(query, scope=scope)
        hits = self._retriever.search(query)
        return [
            hit
            for hit in hits
            if hit.record.scope is MemoryScope.SYSTEM
            or hit.record.owner_id == context.identity_for(hit.record.scope)
        ]

    def update(self, record: MemoryRecord, *, context: MemoryAccessContext) -> MemoryRecord:
        existing = next((r for r in self._store.list(record.namespace) if r.memory_id == record.memory_id), None)
        if existing is None:
            raise KeyError(f"Unknown memory: {record.memory_id}")
        self._check_record_access(context, existing)
        if record.owner_id != existing.owner_id or record.scope != existing.scope:
            raise MemoryAccessDenied("Memory ownership and scope are immutable through update")
        if record.memory_id != existing.memory_id:
            raise MemoryAccessDenied("Memory identity is immutable through update")
        self._validate_namespace(existing.namespace)
        return self._store.update(record)

    def update_content(self, memory_id: UUID, content: str, *, context: MemoryAccessContext,
                       source: str | None = None) -> MemoryRecord:
        current = next((r for r in self._store.list() if r.memory_id == memory_id), None)
        if current is None:
            raise KeyError(f"Unknown memory: {memory_id}")
        self._check_record_access(context, current)
        return self._store.update_content(memory_id, content, source=source)

    def forget(self, memory_id: UUID, *, context: MemoryAccessContext) -> bool:
        current = next((r for r in self._store.list() if r.memory_id == memory_id), None)
        if current is None:
            return False
        self._check_record_access(context, current)
        return self._store.forget(memory_id)
