import pytest

from aios.runtime.event_store import InMemoryEventStore
from aios.runtime.events import RuntimeEvent


@pytest.mark.asyncio
async def test_event_store_appends_queries_and_replays() -> None:
    store = InMemoryEventStore()
    await store.append(RuntimeEvent("workflow.started", {"n": 1}, correlation_id="wf-1"))
    await store.append(RuntimeEvent("tool.called", {"n": 2}, correlation_id="wf-1"))
    await store.append(RuntimeEvent("workflow.started", {"n": 3}, correlation_id="wf-2"))

    events = await store.list(correlation_id="wf-1")
    assert [event.type for event in events] == ["workflow.started", "tool.called"]

    replayed = []
    await store.replay(replayed.append, event_type="workflow.started")
    assert [event.payload["n"] for event in replayed] == [1, 3]
