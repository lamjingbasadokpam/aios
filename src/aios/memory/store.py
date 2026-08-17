"""Provider-neutral agent memory store with an in-memory V1 backend."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
from uuid import UUID

from .contracts import MemoryQuery, MemoryRecord, MemoryScope, MemoryType


class MemoryStore:
    """Memory lifecycle boundary; persistence remains implementation-neutral."""

    def __init__(self) -> None:
        self._records: list[MemoryRecord] = []

    def add(self, record: MemoryRecord) -> MemoryRecord:
        self._records.append(record)
        return record

    def list(self, namespace: str = "default") -> list[MemoryRecord]:
        now = datetime.now(timezone.utc)
        return [record for record in self._records if record.namespace == namespace and not record.is_expired(now=now)]

    def query_candidates(self, query: MemoryQuery) -> list[MemoryRecord]:
        records = self.list(query.namespace)
        if query.memory_type is not None:
            records = [r for r in records if r.memory_type == query.memory_type]
        if query.scope is not None:
            records = [r for r in records if r.scope == query.scope]
        if query.metadata_filter:
            records = [r for r in records if all(r.metadata.get(k) == value for k, value in query.metadata_filter.items())]
        return records

    def remember(
        self,
        content: str,
        *,
        source: str,
        namespace: str = "default",
        metadata: dict | None = None,
        memory_type: MemoryType = MemoryType.SEMANTIC,
        scope: MemoryScope = MemoryScope.AGENT,
        owner_id: UUID | None = None,
        expires_at: datetime | None = None,
        supersedes_id: UUID | None = None,
    ) -> MemoryRecord:
        record = MemoryRecord(
            content=content,
            source=source,
            namespace=namespace,
            metadata=metadata or {},
            memory_type=memory_type,
            scope=scope,
            owner_id=owner_id,
            expires_at=expires_at,
            supersedes_id=supersedes_id,
        )
        return self.add(record)

    def update(self, record: MemoryRecord) -> MemoryRecord:
        for index, current in enumerate(self._records):
            if current.memory_id == record.memory_id:
                self._records[index] = record
                return record
        raise KeyError(f"Unknown memory: {record.memory_id}")

    def update_content(self, memory_id: UUID, content: str, *, source: str | None = None) -> MemoryRecord:
        current = next((r for r in self._records if r.memory_id == memory_id), None)
        if current is None:
            raise KeyError(f"Unknown memory: {memory_id}")
        return self.update(replace(current, content=content, source=source or current.source))

    def forget(self, memory_id: UUID) -> bool:
        for index, record in enumerate(self._records):
            if record.memory_id == memory_id:
                del self._records[index]
                return True
        return False

    def search_text(self, query: str, *, namespace: str = "default", limit: int = 5) -> list[MemoryRecord]:
        if limit <= 0:
            return []
        terms = {term.lower() for term in query.split() if term.strip()}
        candidates = self.list(namespace)
        ranked = sorted(candidates, key=lambda record: sum(term in record.content.lower() for term in terms), reverse=True)
        return [record for record in ranked if not terms or any(term in record.content.lower() for term in terms)][:limit]
