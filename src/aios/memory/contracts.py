"""Provider-independent memory contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class MemoryRecord:
    content: str
    source: str
    memory_id: UUID = field(default_factory=uuid4)
    namespace: str = "default"
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True, slots=True)
class MemoryQuery:
    query: str
    namespace: str = "default"
    top_k: int = 5
    metadata_filter: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class MemoryHit:
    record: MemoryRecord
    score: float
