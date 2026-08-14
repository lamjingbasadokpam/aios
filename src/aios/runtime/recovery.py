"""Crash recovery and lifecycle rehydration for AIOS runs."""

from __future__ import annotations

from dataclasses import dataclass

from .events import RuntimeEvent
from .lifecycle import LifecycleState, RuntimeRun


@dataclass(frozen=True, slots=True)
class RecoveryResult:
    run_id: str
    state: LifecycleState
    event_count: int
    recoverable: bool
    reason: str


class RuntimeRecovery:
    """Reconstructs a run's lifecycle state from its durable event history."""

    _STATE_MAP = {state.value: state for state in LifecycleState}

    def rehydrate(self, events: list[RuntimeEvent], run: RuntimeRun) -> RecoveryResult:
        if not events:
            return RecoveryResult(run.run.run_id, run.state, 0, False, "no durable history")

        for event in events:
            state_value = event.payload.get("state")
            state = self._STATE_MAP.get(state_value) if isinstance(state_value, str) else None
            if state is not None:
                run.state = state

        recoverable = run.state in {
            LifecycleState.ADMITTED,
            LifecycleState.RESERVED,
            LifecycleState.RUNNING,
            LifecycleState.SETTLING,
        }
        if run.state == LifecycleState.RUNNING:
            reason = "rehydrated running run; reconcile before resume"
        elif recoverable:
            reason = "rehydrated from durable history"
        else:
            reason = f"terminal state: {run.state.value}"
        return RecoveryResult(run.run.run_id, run.state, len(events), recoverable, reason)
