"""Lifecycle tracking for recovery alerts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .recovery_alert_events import RecoveryAlertEvent


@dataclass(frozen=True, slots=True)
class RecoveryAlertLifecycle:
    code: str
    threshold: float | int
    active: bool
    last_event: RecoveryAlertEvent


class RecoveryAlertLifecycleTracker:
    """Tracks active/resolved alert state from ordered alert events."""

    _NON_ALERT_EVENTS = frozenset({"incident_resolved"})

    def update(self, events: Iterable[RecoveryAlertEvent]) -> dict[tuple[str, float | int], RecoveryAlertLifecycle]:
        current: dict[tuple[str, float | int], RecoveryAlertLifecycle] = {}
        for event in events:
            if event.code in self._NON_ALERT_EVENTS:
                continue
            resolved = event.code.startswith("resolved:")
            code = event.code.removeprefix("resolved:") if resolved else event.code
            key = (code, event.threshold)
            current[key] = RecoveryAlertLifecycle(code, event.threshold, not resolved, event)
        return current

    @staticmethod
    def resolution_event(alert: RecoveryAlertEvent) -> RecoveryAlertEvent:
        return RecoveryAlertEvent(
            f"resolved:{alert.code}",
            f"resolved: {alert.message}",
            alert.value,
            alert.threshold,
        )
