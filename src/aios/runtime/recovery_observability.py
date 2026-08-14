"""Structured observability for effect recovery lifecycle."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable


@dataclass(frozen=True, slots=True)
class RecoveryObservation:
    effect_key: str
    state: str
    reason: str
    owner: str | None = None
    attempt: int = 0
    started_at: datetime | None = None
    resolved_at: datetime | None = None
    result: Any = None

    @property
    def recovery_duration_seconds(self) -> float | None:
        if self.started_at is None or self.resolved_at is None:
            return None
        return max(0.0, (self.resolved_at - self.started_at).total_seconds())


class RecoveryObserver:
    """Emits structured recovery observations without coupling to a metrics backend."""

    def __init__(self, emit: Callable[[RecoveryObservation], None]) -> None:
        self._emit = emit

    def observe(self, observation: RecoveryObservation) -> None:
        self._emit(observation)
