"""Core Agent and Task domain models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class AgentStatus(StrEnum):
    CREATED = "created"
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    FAILED = "failed"
    DISABLED = "disabled"


class TaskStatus(StrEnum):
    CREATED = "created"
    READY = "ready"
    RUNNING = "running"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


@dataclass(slots=True)
class Agent:
    name: str
    agent_id: UUID = field(default_factory=uuid4)
    version: str = "0.1.0"
    status: AgentStatus = AgentStatus.CREATED
    capabilities: set[str] = field(default_factory=set)
    policy_ref: str | None = None
    model_requirements: dict[str, Any] = field(default_factory=dict)
    memory_policy: dict[str, Any] = field(default_factory=dict)
    skill_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=utc_now)


@dataclass(slots=True)
class Task:
    input: str
    task_id: UUID = field(default_factory=uuid4)
    parent_task_id: UUID | None = None
    agent_id: UUID | None = None
    status: TaskStatus = TaskStatus.CREATED
    constraints: dict[str, Any] = field(default_factory=dict)
    requirements: dict[str, Any] = field(default_factory=dict)
    environment_ref: str | None = None
    result: Any = None
    error: str | None = None
    created_at: datetime = field(default_factory=utc_now)
    started_at: datetime | None = None
    completed_at: datetime | None = None
