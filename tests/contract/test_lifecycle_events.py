from aios.runtime.control import InMemoryRuntimeController
from aios.runtime.lifecycle import LifecycleState, RuntimeLifecycle
from aios.runtime.lifecycle_events import LifecycleEventEmitter
from aios.runtime.budget import ResourceBudget
from aios.runtime.reservation import ReservationManager


def test_lifecycle_event_contains_run_and_state() -> None:
    lifecycle = RuntimeLifecycle(InMemoryRuntimeController(), ReservationManager(ResourceBudget(max_tool_calls=2)))
    run = lifecycle.create("run-1")
    event = LifecycleEventEmitter().transition(run, LifecycleState.ADMITTED)
    assert event.type == "run.admitted"
    assert event.run_id == "run-1"
    assert event.payload["state"] == "admitted"
