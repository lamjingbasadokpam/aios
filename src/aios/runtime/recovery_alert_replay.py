"""Replay and deduplicate durable recovery alerts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .recovery_alert_events import RecoveryAlertEvent


@dataclass(frozen=True, slots=True)
class RecoveryAlertIdentity:
    code: str
    threshold: float | int


class RecoveryAlertReplayer:
    """Keeps one logical alert identity from being emitted repeatedly during replay."""

    def replay(self, events: Iterable[RecoveryAlertEvent]) -> list[RecoveryAlertEvent]:
        seen: set[RecoveryAlertIdentity] = set()
        result: list[RecoveryAlertEvent] = []
        for event in events:
            identity = RecoveryAlertIdentity(event.code, event.threshold)
            if identity in seen:
                continue
            seen.add(identity)
            result.append(event)
        return result
