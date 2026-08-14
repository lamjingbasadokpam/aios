import pytest

from aios.runtime.durable_history import DurableLifecycleHistory
from aios.runtime.events import RuntimeEvent


class Store:
    def __init__(self) -> None:
        self.events = []

    async def append(self, event):
        self.events.append(event)

    async def for_run(self, run_id):
        return [event for event in self.events if event.run_id == run_id]


@pytest.mark.asyncio
async def test_history_round_trips_lifecycle_events() -> None:
    store = Store()
    history = DurableLifecycleHistory(store)
    event = RuntimeEvent(
        event_id="e1", type="run.created", timestamp="2026-01-01T00:00:00Z", source="test", run_id="run-1", payload={}
    )
    await history.append(event)
    assert await history.history("run-1") == [event]
    assert await history.history("other") == []
