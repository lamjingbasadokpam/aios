import pytest

from aios.worker import AgentWorkerRuntime, WorkerContext


class Handler:
    async def handle(self, operation, payload):
        return {"operation": operation, "payload": payload}


@pytest.mark.asyncio
async def test_worker_dispatch_requires_running_runtime() -> None:
    worker = AgentWorkerRuntime(WorkerContext("coder", "local/default"), Handler())
    with pytest.raises(RuntimeError):
        await worker.dispatch("ping", {})
    await worker.start()
    assert await worker.dispatch("ping", {"x": 1}) == {"operation": "ping", "payload": {"x": 1}}
    await worker.stop()
    assert worker.running is False
