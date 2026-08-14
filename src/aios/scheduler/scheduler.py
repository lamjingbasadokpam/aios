"""Local scheduler for delayed and recurring tasks."""

from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone
from typing import Any

from .contracts import QueueItem, ScheduledTask
from .queue import TaskQueue


class Scheduler:
    def __init__(self, max_concurrency: int = 4) -> None:
        if max_concurrency < 1:
            raise ValueError("max_concurrency must be >= 1")
        self.queue = TaskQueue()
        self.max_concurrency = max_concurrency
        self._running = False
        self._tasks: set[asyncio.Task] = set()
        self._run_counts: dict = {}

    def schedule(self, task: ScheduledTask) -> None:
        self.queue.push(QueueItem(task))

    async def _execute(self, task: ScheduledTask, context: dict[str, Any]) -> None:
        try:
            await task.handler(dict(context))
        finally:
            count = self._run_counts.get(task.task_id, 0) + 1
            self._run_counts[task.task_id] = count
            if task.interval_seconds is not None and (task.max_runs is None or count < task.max_runs):
                next_run = datetime.now(timezone.utc) + timedelta(seconds=task.interval_seconds)
                self.schedule(ScheduledTask(
                    name=task.name,
                    handler=task.handler,
                    run_at=next_run,
                    priority=task.priority,
                    task_id=task.task_id,
                    interval_seconds=task.interval_seconds,
                    max_runs=task.max_runs,
                ))

    async def run_once(self, context: dict[str, Any] | None = None) -> int:
        started = 0
        while len(self._tasks) < self.max_concurrency:
            item = self.queue.pop_ready()
            if item is None:
                break
            task = asyncio.create_task(self._execute(item.task, context or {}))
            self._tasks.add(task)
            task.add_done_callback(self._tasks.discard)
            started += 1
        if self._tasks:
            await asyncio.gather(*tuple(self._tasks), return_exceptions=True)
        return started

    async def run(self, poll_interval_seconds: float = 1.0, context: dict[str, Any] | None = None) -> None:
        if poll_interval_seconds <= 0:
            raise ValueError("poll_interval_seconds must be > 0")
        self._running = True
        while self._running:
            await self.run_once(context)
            await asyncio.sleep(poll_interval_seconds)

    def stop(self) -> None:
        self._running = False
