import asyncio

from aios.supervisor import Supervisor, SupervisorPolicy
from aios.workers import WorkerManager, WorkerSpec, WorkerStatus


def test_supervisor_restarts_failed_worker() -> None:
    attempts = 0

    async def run(state):
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise RuntimeError("transient")
        await asyncio.sleep(0.05)

    async def scenario():
        manager = WorkerManager()
        state = manager.register(WorkerSpec("restartable", run))
        await manager.start(state.spec.worker_id)
        await asyncio.sleep(0.01)
        supervisor = Supervisor(manager, SupervisorPolicy(restart_failed=True, max_restarts=1, restart_backoff_seconds=0))
        await supervisor.check_once()
        await asyncio.sleep(0.01)
        assert attempts == 2
        assert state.status == WorkerStatus.RUNNING

    asyncio.run(scenario())


def test_supervisor_detects_missing_worker() -> None:
    async def scenario():
        manager = WorkerManager()
        report = Supervisor(manager).health("missing")
        assert not report.healthy

    asyncio.run(scenario())
