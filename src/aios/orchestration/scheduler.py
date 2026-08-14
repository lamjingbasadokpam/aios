"""Bounded dependency-aware task scheduler."""

from __future__ import annotations

import asyncio
from typing import Any

from .contracts import OrchestrationTask, TaskResult, TaskState
from .graph import TaskGraph


class Orchestrator:
    def __init__(self, graph: TaskGraph, max_concurrency: int = 4) -> None:
        if max_concurrency < 1:
            raise ValueError("max_concurrency must be >= 1")
        self.graph = graph
        self.max_concurrency = max_concurrency

    async def run(self, initial_context: dict[str, Any] | None = None) -> dict:
        self.graph.validate()
        context = dict(initial_context or {})
        results: dict = {}
        pending = {task.task_id: task for task in self.graph.tasks()}
        semaphore = asyncio.Semaphore(self.max_concurrency)

        async def execute(task: OrchestrationTask) -> TaskResult:
            attempts = 0
            while True:
                attempts += 1
                try:
                    async with semaphore:
                        output = await task.handler(dict(context))
                    return TaskResult(task.task_id, TaskState.SUCCEEDED, output, attempts=attempts)
                except Exception as exc:
                    if attempts > task.retry_limit:
                        return TaskResult(task.task_id, TaskState.FAILED, error=str(exc), attempts=attempts)

        while pending:
            ready = [
                task for task in pending.values()
                if all(dep in results and results[dep].state == TaskState.SUCCEEDED for dep in task.dependencies)
            ]
            blocked = [
                task for task in pending.values()
                if any(dep in results and results[dep].state != TaskState.SUCCEEDED for dep in task.dependencies)
            ]
            if blocked and not ready:
                for task in blocked:
                    results[task.task_id] = TaskResult(task.task_id, TaskState.CANCELLED, error="Dependency failed")
                    pending.pop(task.task_id)
                continue
            if not ready:
                raise RuntimeError("Orchestration made no progress")

            batch = await asyncio.gather(*(execute(task) for task in ready))
            for task, result in zip(ready, batch):
                results[task.task_id] = result
                pending.pop(task.task_id)
                if result.state == TaskState.SUCCEEDED:
                    context[str(task.task_id)] = result.output

        return results
