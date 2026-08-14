from aios.runtime.control import InMemoryRuntimeController
from aios.runtime.lifecycle import LifecycleState, RuntimeLifecycle
from aios.runtime.recovery import RuntimeRecovery
from aios.runtime.reservation import ReservationManager
from aios.runtime.budget import ResourceBudget
from aios.runtime.events import RuntimeEvent


def test_recovery_rehydrates_latest_lifecycle_state() -> None:
    lifecycle = RuntimeLifecycle(InMemoryRuntimeController(), ReservationManager(ResourceBudget()))
    run = lifecycle.create("run-1")
    events = [
        RuntimeEvent("e1", "run.created", "t", "test", "run-1", {"state": "created"}),
        RuntimeEvent("e2", "run.running", "t", "test", "run-1", {"state": "running"}),
    ]
    result = RuntimeRecovery().rehydrate(events, run)
    assert result.state == LifecycleState.RUNNING
    assert result.recoverable is True
    assert result.event_count == 2


def test_recovery_marks_terminal_run_non_recoverable() -> None:
    lifecycle = RuntimeLifecycle(InMemoryRuntimeController(), ReservationManager(ResourceBudget()))
    run = lifecycle.create("run-2")
    events = [RuntimeEvent("e1", "run.completed", "t", "test", "run-2", {"state": "completed"})]
    result = RuntimeRecovery().rehydrate(events, run)
    assert result.state == LifecycleState.COMPLETED
    assert result.recoverable is False
