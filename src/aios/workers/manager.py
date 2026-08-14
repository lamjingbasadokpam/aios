"""Local worker lifecycle manager."""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone

from .contracts import WorkerSpec, WorkerState, WorkerStatus


class WorkerManager:
    def __init__(self, max_workers: int = 8) -> None:
        if max_workers < 1:
            raise ValueError("max_workers must be >= 1")
        self.max_workers = max_workers
        self._workers: dict = {}
        self._tasks: dict = {}
        self._lock = asyncio.Lock()

    def register(self, spec: WorkerSpec) -> WorkerState:
        if spec.worker_id in self._workers:
            raise ValueError(f"Worker already registered: {spec.worker_id}")
        if len(self._workers) >= self.max_workers:
            raise RuntimeError("Worker capacity reached")
        state = WorkerState(spec=spec)
        self._workers[spec.worker_id] = state
        return state

    def get(self, worker_id):
        return self._workers.get(worker_id)

    async def start(self, worker_id) -> WorkerState:
        state = self._workers[worker_id]
        if state.status not in {WorkerStatus.CREATED, WorkerStatus.STOPPED}:
            raise RuntimeError(f"Worker cannot start from state {state.status}")
        state.status = WorkerStatus.STARTING
        state.started_at = datetime.now(timezone.utc)
        state.heartbeat()
        task = asyncio.create_task(self._run(state))
        self._tasks[worker_id] = task
        return state

    async def _run(self, state: WorkerState) -> None:
        try:
            state.status = WorkerStatus.RUNNING
            await state.spec.run(state)
            if state.status != WorkerStatus.STOPPING:
                state.status = WorkerStatus.STOPPED
        except asyncio.CancelledError:
            state.status = WorkerStatus.STOPPED
            raise
        except Exception as exc:
            state.metadata["error"] = str(exc)
            state.status = WorkerStatus.FAILED

    async def stop(self, worker_id) -> WorkerState:
        state = self._workers[worker_id]
        task = self._tasks.get(worker_id)
        if task and not task.done():
            state.status = WorkerStatus.STOPPING
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
        state.status = WorkerStatus.STOPPED
        return state

    async def stop_all(self) -> None:
        await asyncio.gather(*(self.stop(worker_id) for worker_id in list(self._workers)), return_exceptions=True)

    def snapshot(self) -> list[WorkerState]:
        return list(self._workers.values())
