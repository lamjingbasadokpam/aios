"""Post-crash reconciliation decisions for rehydrated AIOS runs."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .budget import ResourceUsage
from .lifecycle import LifecycleState, RuntimeRun
from .reservation import ReservationManager


class RecoveryAction(str, Enum):
    RESUME = "resume"
    CANCEL = "cancel"
    FAIL = "fail"
    RECONCILE = "reconcile"


@dataclass(frozen=True, slots=True)
class ReconciliationInput:
    current_usage: ResourceUsage
    cancellation_requested: bool = False
    external_action_in_flight: bool = False
    last_event_consistent: bool = True


@dataclass(frozen=True, slots=True)
class ReconciliationResult:
    action: RecoveryAction
    reason: str


class RecoveryReconciler:
    """Conservatively decides whether a recovered run may resume."""

    def __init__(self, reservations: ReservationManager) -> None:
        self.reservations = reservations

    def reconcile(self, run: RuntimeRun, state: ReconciliationInput) -> ReconciliationResult:
        if not state.last_event_consistent:
            return ReconciliationResult(RecoveryAction.FAIL, "durable history is inconsistent")
        if state.cancellation_requested or run.cancellation.cancelled:
            return ReconciliationResult(RecoveryAction.CANCEL, "cancellation was requested")
        if state.external_action_in_flight:
            return ReconciliationResult(RecoveryAction.RECONCILE, "external action may have committed; resolve before retry")
        if run.state not in {LifecycleState.ADMITTED, LifecycleState.RESERVED, LifecycleState.RUNNING, LifecycleState.SETTLING}:
            return ReconciliationResult(RecoveryAction.FAIL, f"state {run.state.value} is not recoverable")
        if not self.reservations._within_budget(state.current_usage):
            return ReconciliationResult(RecoveryAction.FAIL, "current usage exceeds available budget")
        return ReconciliationResult(RecoveryAction.RESUME, "recovered run is safe to resume")
