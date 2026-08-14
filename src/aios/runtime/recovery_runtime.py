"""Runtime lifecycle integration for recovery-gated startup."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .effect_recovery_events import EffectRecoveryEvent
from .recovery_gate import RecoveryResumeGate
from .recovery_state import RecoveryState, RecoveryStateRehydrator


class RecoveryMode(str):
    NORMAL = "normal"
    RECOVERY_REQUIRED = "recovery_required"


@dataclass(frozen=True, slots=True)
class RuntimeRecoveryStatus:
    mode: str
    state: RecoveryState


class RecoveryRuntimeController:
    """Integrates event rehydration and the resume gate into runtime startup."""

    def __init__(
        self,
        rehydrator: RecoveryStateRehydrator | None = None,
        gate: RecoveryResumeGate | None = None,
    ) -> None:
        self.rehydrator = rehydrator or RecoveryStateRehydrator()
        self.gate = gate or RecoveryResumeGate(self.rehydrator)

    def startup(self, events: Iterable[EffectRecoveryEvent]) -> RuntimeRecoveryStatus:
        state = self.rehydrator.rehydrate(events)
        decision = self.gate.evaluate(state)
        mode = RecoveryMode.NORMAL if decision.allowed else RecoveryMode.RECOVERY_REQUIRED
        return RuntimeRecoveryStatus(mode, state)

    def require_execution(self, status: RuntimeRecoveryStatus) -> None:
        if status.mode != RecoveryMode.NORMAL:
            raise RuntimeError("runtime execution blocked: recovery is required")
