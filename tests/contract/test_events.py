import asyncio
from uuid import uuid4

import pytest

from aios.events import Event, EventBus, ExecutionState, StateStore


def test_event_bus_delivers_to_topic_subscribers() -> None:
    seen = []

    async def handler(event):
        seen.append(event.payload["value"])

    bus = EventBus()
    bus.subscribe("task.completed", handler)
    asyncio.run(bus.publish(Event(topic="task.completed", payload={"value": 42})))
    assert seen == [42]


def test_state_store_versions_and_conflicts() -> None:
    store = StateStore()
    execution_id = uuid4()
    state = store.put(ExecutionState(execution_id, "running", step=1))
    assert state.version == 1
    updated = store.put(ExecutionState(execution_id, "running", step=2), expected_version=1)
    assert updated.version == 2
    with pytest.raises(RuntimeError):
        store.put(ExecutionState(execution_id, "done"), expected_version=1)
