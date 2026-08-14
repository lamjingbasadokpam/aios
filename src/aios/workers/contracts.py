"""Worker lifecycle contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Awaitable, Callable
from uuid import UUID, uuid4


class WorkerStatus(str, Enum):
    CREATED = "created"
    STARTING = "starting"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPING = "stopping"
    STOPPED = "stopped"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class WorkerSpec:
    name: str
    run: Callable[["WorkerState"], Awaitable[None]]
    heartbeat_seconds: float = 10.0
    worker_id: UUID = field(default_factory=uuid4)


@dataclass(slots=True)
class WorkerState:
    spec: WorkerSpec
    status: WorkerStatus = WorkerStatus.CREATED
    started_at: datetime | None = None
    last_heartbeat: datetime | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def heartbeat(self) -> None:
        self.last_heartbeat = datetime.now(timezone.utc)
