"""Storage interfaces shared by durable AIOS components."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Protocol
from uuid import UUID


@dataclass(frozen=True, slots=True)
class StoredExecution:
    execution_id: UUID
    status: str
    step: int
    checkpoint: dict[str, Any]
    version: int
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True, slots=True)
class StoredWorker:
    worker_id: UUID
    name: str
    status: str
    metadata: dict[str, Any]
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True, slots=True)
class EventRecord:
    event_id: UUID
    topic: str
    payload: dict[str, Any]
    occurred_at: datetime
    sequence: int


class StorageBackend(Protocol):
    async def save_execution(self, execution: StoredExecution) -> StoredExecution: ...
    async def get_execution(self, execution_id: UUID) -> StoredExecution | None: ...
    async def save_worker(self, worker: StoredWorker) -> StoredWorker: ...
    async def get_worker(self, worker_id: UUID) -> StoredWorker | None: ...
    async def append_event(self, event: EventRecord) -> EventRecord: ...
    async def events_since(self, sequence: int = 0) -> list[EventRecord]: ...
