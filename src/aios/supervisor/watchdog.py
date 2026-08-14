"""Local worker supervisor with heartbeat checks and bounded restarts."""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone

from aios.workers import WorkerManager, WorkerStatus

from .contracts import SupervisorPolicy, WorkerHealth


class Supervisor:
    def __init__(self, manager: WorkerManager, policy: SupervisorPolicy | None = None) -> None:
        self.manager = manager
        self.policy = policy or SupervisorPolicy()
        self._restart_counts: dict = {}
        self._stopped = asyncio.Event()

    def health(self, worker_id) -> WorkerHealth:
        state = self.manager.get(worker_id)
        now = datetime.now(timezone.utc)
        if state is None:
            return WorkerHealth(worker_id, False, "worker not registered", now)
        if state.status == WorkerStatus.FAILED:
            return WorkerHealth(worker_id, False, "worker failed", now)
        if state.status == WorkerStatus.RUNNING and state.last_heartbeat:
            age = (now - state.last_heartbeat).total_seconds()
            if age > self.policy.heartbeat_timeout_seconds:
                return WorkerHealth(worker_id, False, "heartbeat timeout", now)
        return WorkerHealth(worker_id, state.status in {WorkerStatus.RUNNING, WorkerStatus.STARTING},
                            f"status={state.status.value}", now)

    async def check_once(self) -> list[WorkerHealth]:
        reports = []
        for state in self.manager.snapshot():
            report = self.health(state.spec.worker_id)
            reports.append(report)
            if not report.healthy and self.policy.restart_failed:
                count = self._restart_counts.get(state.spec.worker_id, 0)
                if count < self.policy.max_restarts and state.status == WorkerStatus.FAILED:
                    self._restart_counts[state.spec.worker_id] = count + 1
                    await asyncio.sleep(self.policy.restart_backoff_seconds)
                    await self.manager.start(state.spec.worker_id)
        return reports

    async def run(self, interval_seconds: float = 5.0) -> None:
        if interval_seconds <= 0:
            raise ValueError("interval_seconds must be > 0")
        self._stopped.clear()
        while not self._stopped.is_set():
            await self.check_once()
            try:
                await asyncio.wait_for(self._stopped.wait(), timeout=interval_seconds)
            except asyncio.TimeoutError:
                pass

    def stop(self) -> None:
        self._stopped.set()
