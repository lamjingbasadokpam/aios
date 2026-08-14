"""Durable event representation for recovery alerts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .recovery_alerts import RecoveryAlert


@dataclass(frozen=True, slots=True)
class RecoveryAlertEvent:
    code: str
    message: str
    value: float | int
    threshold: float | int

    @classmethod
    def from_alert(cls, alert: RecoveryAlert) -> "RecoveryAlertEvent":
        return cls(alert.code, alert.message, alert.value, alert.threshold)


class RecoveryAlertEventSink:
    """Adapter for persisting alert events through the runtime event store."""

    def __init__(self, append_event: Callable[[str, dict[str, Any]], None]) -> None:
        self._append_event = append_event

    def emit(self, event: RecoveryAlertEvent) -> None:
        self._append_event(
            "recovery_alert",
            {
                "code": event.code,
                "message": event.message,
                "value": event.value,
                "threshold": event.threshold,
            },
        )
