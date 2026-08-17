"""Provider-independent memory contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import UUID, uuid4


class MemoryType(str, Enum):
    """Semantic role of a memory record."""

    WORKING = "working"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    PROCEDURAL = "procedural"


class MemoryScope(str, Enum):
    """Ownership/lifetime scope of a memory record."""

    SYSTEM = "system"
    AGENT = "agent"
    SESSION = "session"
    USER = "user"
    TASK = "task"


@dataclass(frozen=True, slots=True)
class MemoryRecord:
    content: str
    source: str
    memory_id: UUID = field(default_factory=uuid4)
    namespace: str = "default"
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    memory_type: MemoryType = MemoryType.SEMANTIC
    scope: MemoryScope = MemoryScope.AGENT
    owner_id: UUID | None = None
    expires_at: datetime | None = None
    supersedes_id: UUID | None = None

    def is_expired(self, *, now: datetime | None = None) -> bool:
        if self.expires_at is None:
            return False
        current = now or datetime.now(timezone.utc)
        return self.expires_at <= current


@dataclass(frozen=True, slots=True)
class MemoryQuery:
    query: str
    namespace: str = "default"
    top_k: int = 5
    metadata_filter: dict[str, Any] = field(default_factory=dict)
    memory_type: MemoryType | None = None
    scope: MemoryScope | None = None


@dataclass(frozen=True, slots=True)
class MemoryHit:
    record: MemoryRecord
    score: float
