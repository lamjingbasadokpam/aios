"""Scheduling and durable queue contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import IntEnum, StrEnum
from typing import Any, Awaitable, Callable
from uuid import UUID, uuid4


class TaskPriority(IntEnum):
    LOW = 30
    NORMAL = 20
    HIGH = 10
    CRITICAL = 0


class QueueStatus(StrEnum):
    READY = "ready"
    LEASED = "leased"
    COMPLETE = "complete"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class ScheduledTask:
    name: str
    handler: Callable[[dict[str, Any]], Awaitable[Any]]
    run_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    priority: TaskPriority = TaskPriority.NORMAL
    task_id: UUID = field(default_factory=uuid4)
    interval_seconds: float | None = None
    max_runs: int | None = None


@dataclass(frozen=True, slots=True)
class QueueItem:
    task: ScheduledTask
    enqueued_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    status: QueueStatus = QueueStatus.READY
    lease_owner: str | None = None
    lease_until: datetime | None = None
    attempts: int = 0

    def next_run(self) -> datetime | None:
        if self.task.interval_seconds is None:
            return None
        return self.task.run_at + timedelta(seconds=self.task.interval_seconds)
