"""Stable orchestration contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Awaitable, Callable
from uuid import UUID, uuid4


class TaskState(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(frozen=True, slots=True)
class OrchestrationTask:
    name: str
    handler: Callable[[dict[str, Any]], Awaitable[Any]]
    task_id: UUID = field(default_factory=uuid4)
    dependencies: tuple[UUID, ...] = ()
    retry_limit: int = 0


@dataclass(frozen=True, slots=True)
class TaskResult:
    task_id: UUID
    state: TaskState
    output: Any = None
    error: str | None = None
    attempts: int = 0
