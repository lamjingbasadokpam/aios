"""Dependency graph for orchestrated tasks."""

from __future__ import annotations

from .contracts import OrchestrationTask


class TaskGraph:
    def __init__(self) -> None:
        self._tasks: dict = {}

    def add(self, task: OrchestrationTask) -> None:
        if task.task_id in self._tasks:
            raise ValueError(f"Task already exists: {task.task_id}")
        self._tasks[task.task_id] = task

    def get(self, task_id):
        return self._tasks.get(task_id)

    def tasks(self) -> list[OrchestrationTask]:
        return list(self._tasks.values())

    def validate(self) -> None:
        ids = set(self._tasks)
        for task in self._tasks.values():
            missing = set(task.dependencies) - ids
            if missing:
                raise ValueError(f"Task {task.name} has missing dependencies: {missing}")

        visiting: set = set()
        visited: set = set()

        def visit(task_id) -> None:
            if task_id in visiting:
                raise ValueError("Task graph contains a cycle")
            if task_id in visited:
                return
            visiting.add(task_id)
            for dependency in self._tasks[task_id].dependencies:
                visit(dependency)
            visiting.remove(task_id)
            visited.add(task_id)

        for task_id in self._tasks:
            visit(task_id)
