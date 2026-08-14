from datetime import datetime, timezone
from uuid import uuid4

import asyncio

from aios.storage import EventRecord, InMemoryStorage, StoredExecution, StoredWorker


def test_storage_persists_execution_worker_and_events() -> None:
    async def scenario():
        store = InMemoryStorage()
        execution_id = uuid4()
        worker_id = uuid4()
        await store.save_execution(StoredExecution(execution_id, "running", 2, {"x": 1}, 3))
        await store.save_worker(StoredWorker(worker_id, "worker-a", "running", {}))
        event = await store.append_event(EventRecord(uuid4(), "task.completed", {"id": "x"}, datetime.now(timezone.utc), 0))
        assert (await store.get_execution(execution_id)).checkpoint == {"x": 1}
        assert (await store.get_worker(worker_id)).name == "worker-a"
        assert event.sequence == 1
        assert len(await store.events_since(0)) == 1

    asyncio.run(scenario())
