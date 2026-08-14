"""Safe completion and exit from runtime recovery mode."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .effect_recovery_events import EffectRecoveryEvent, EffectRecoveryEventType
from .recovery_gate import RecoveryResumeGate
from .recovery_state import RecoveryStateRehydrator


@dataclass(frozen=True, slots=True)
class RecoveryCompletion:
    completed: bool
    reason: str


class RecoveryCompletionCoordinator:
    """Determines whether persisted recovery history is now safe to resume."""

    def __init__(self, rehydrator: RecoveryStateRehydrator | None = None) -> None:
        self.rehydrator = rehydrator or RecoveryStateRehydrator()
        self.gate = RecoveryResumeGate(self.rehydrator)

    def complete(self, events: Iterable[EffectRecoveryEvent]) -> RecoveryCompletion:
        state = self.rehydrator.rehydrate(events)
        decision = self.gate.evaluate(state)
        if decision.allowed:
            return RecoveryCompletion(True, "all recovered effects are safe to resume")
        return RecoveryCompletion(False, "one or more effects still require reconciliation")

    @staticmethod
    def resolution_event(key: str, result: object) -> EffectRecoveryEvent:
        return EffectRecoveryEvent(
            EffectRecoveryEventType.EFFECT_REUSED,
            key,
            "recovery reconciled and effect outcome confirmed",
            result,
        )
