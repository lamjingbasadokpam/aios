import asyncio

from aios.workers import WorkerManager, WorkerSpec, WorkerStatus


def test_worker_starts_and_stops() -> None:
    async def run(state):
        state.heartbeat()
        await asyncio.sleep(0.2)

    async def scenario():
        manager = WorkerManager(max_workers=1)
        state = manager.register(WorkerSpec("test", run))
        await manager.start(state.spec.worker_id)
        await asyncio.sleep(0.01)
        assert state.status == WorkerStatus.RUNNING
        await manager.stop(state.spec.worker_id)
        assert state.status == WorkerStatus.STOPPED

    asyncio.run(scenario())


def test_worker_failure_is_recorded() -> None:
    async def run(state):
        raise RuntimeError("boom")

    async def scenario():
        manager = WorkerManager()
        state = manager.register(WorkerSpec("bad", run))
        await manager.start(state.spec.worker_id)
        await asyncio.sleep(0.01)
        assert state.status == WorkerStatus.FAILED
        assert state.metadata["error"] == "boom"

    asyncio.run(scenario())
