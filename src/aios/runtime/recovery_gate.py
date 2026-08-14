"""Enforce recovery safety before runtime execution resumes."""

from __future__ import annotations

from dataclasses import dataclass

from .recovery_state import RecoveryState, RecoveryStateRehydrator


@dataclass(frozen=True, slots=True)
class RecoveryGateDecision:
    allowed: bool
    reason: str


class RecoveryResumeGate:
    """Runtime enforcement point for startup recovery state."""

    def __init__(self, rehydrator: RecoveryStateRehydrator | None = None) -> None:
        self.rehydrator = rehydrator or RecoveryStateRehydrator()

    def evaluate(self, state: RecoveryState) -> RecoveryGateDecision:
        if self.rehydrator.is_safe_to_resume(state):
            return RecoveryGateDecision(True, "recovery state is safe to resume")
        return RecoveryGateDecision(False, "one or more effects require reconciliation")

    def require_resume(self, state: RecoveryState) -> None:
        decision = self.evaluate(state)
        if not decision.allowed:
            raise RuntimeError(decision.reason)
