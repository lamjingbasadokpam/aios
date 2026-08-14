"""Replay recovery events into an in-memory effect state projection."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from .effect_recovery_events import EffectRecoveryEvent, EffectRecoveryEventType


@dataclass(slots=True)
class ReplayedEffectState:
    key: str
    state: str = "unknown"
    result: Any = None
    reason: str = ""


class RecoveryEventReplayer:
    """Deterministically rebuilds recovery state from durable recovery events."""

    def replay(self, events: Iterable[EffectRecoveryEvent]) -> dict[str, ReplayedEffectState]:
        state: dict[str, ReplayedEffectState] = {}
        for event in events:
            current = state.setdefault(event.effect_key, ReplayedEffectState(event.effect_key))
            if event.event_type == EffectRecoveryEventType.EFFECT_REUSED:
                current.state = "committed"
                current.result = event.result
            elif event.event_type == EffectRecoveryEventType.EFFECT_RETRIED:
                current.state = "retried"
                current.result = event.result
            elif event.event_type == EffectRecoveryEventType.EFFECT_RECONCILIATION_REQUIRED:
                current.state = "reconciliation_required"
            elif event.event_type == EffectRecoveryEventType.EFFECT_RECOVERY_ABORTED:
                current.state = "aborted"
            current.reason = event.reason
        return state
