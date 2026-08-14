"""Supervisor contracts."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True, slots=True)
class SupervisorPolicy:
    heartbeat_timeout_seconds: float = 30.0
    restart_failed: bool = True
    max_restarts: int = 3
    restart_backoff_seconds: float = 1.0


@dataclass(frozen=True, slots=True)
class WorkerHealth:
    worker_id: object
    healthy: bool
    reason: str
    observed_at: datetime

    @classmethod
    def healthy_now(cls, worker_id: object) -> "WorkerHealth":
        return cls(worker_id, True, "heartbeat healthy", datetime.now(timezone.utc))
