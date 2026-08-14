from aios.runtime.budget import ResourceBudget, ResourceUsage
from aios.runtime.control import InMemoryRuntimeController
from aios.runtime.lifecycle import LifecycleState, RuntimeLifecycle
from aios.runtime.reconciliation import RecoveryAction, RecoveryReconciler, ReconciliationInput
from aios.runtime.reservation import ReservationManager


def _run(state: LifecycleState):
    lifecycle = RuntimeLifecycle(InMemoryRuntimeController(), ReservationManager(ResourceBudget(max_tokens=1000)))
    run = lifecycle.create("run-1")
    run.state = state
    return run, lifecycle.reservations


def test_recovery_resumes_safe_run() -> None:
    run, reservations = _run(LifecycleState.RUNNING)
    result = RecoveryReconciler(reservations).reconcile(run, ReconciliationInput(ResourceUsage(tokens=100)))
    assert result.action == RecoveryAction.RESUME


def test_recovery_cancels_when_requested() -> None:
    run, reservations = _run(LifecycleState.RUNNING)
    result = RecoveryReconciler(reservations).reconcile(run, ReconciliationInput(ResourceUsage(), cancellation_requested=True))
    assert result.action == RecoveryAction.CANCEL


def test_recovery_does_not_duplicate_external_action() -> None:
    run, reservations = _run(LifecycleState.RUNNING)
    result = RecoveryReconciler(reservations).reconcile(run, ReconciliationInput(ResourceUsage(), external_action_in_flight=True))
    assert result.action == RecoveryAction.RECONCILE


def test_recovery_fails_on_inconsistent_history() -> None:
    run, reservations = _run(LifecycleState.RUNNING)
    result = RecoveryReconciler(reservations).reconcile(run, ReconciliationInput(ResourceUsage(), last_event_consistent=False))
    assert result.action == RecoveryAction.FAIL
