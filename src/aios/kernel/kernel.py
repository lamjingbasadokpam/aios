"""AIOS Kernel V0 orchestration of core in-memory services."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from .events import Event, EventBus
from .models import Agent, AgentStatus, Task, TaskStatus, utc_now
from .registry import Registry
from .resources import ResourceRegistry

if TYPE_CHECKING:
    from aios.runtime import AgentRuntime


class Kernel:
    def __init__(self, agent_runtime: AgentRuntime | None = None) -> None:
        self.agents: Registry[Agent] = Registry()
        self.tasks: Registry[Task] = Registry()
        self.resources = ResourceRegistry()
        self.events = EventBus()
        self.agent_runtime = agent_runtime
        self.started = False

    def start(self) -> None:
        if self.started:
            return
        self.started = True
        self.events.publish(Event(type="kernel.started", source="kernel"))

    def stop(self) -> None:
        if not self.started:
            return
        self.started = False
        self.events.publish(Event(type="kernel.stopped", source="kernel"))

    def register_agent(self, agent: Agent) -> Agent:
        if not self.started:
            raise RuntimeError("Kernel is not started")
        agent.status = AgentStatus.READY
        self.agents.add(agent, agent.agent_id)
        self.events.publish(
            Event(type="agent.created", source="kernel", actor_id=agent.agent_id,
                  payload={"name": agent.name})
        )
        return agent

    def create_task(self, task: Task) -> Task:
        if not self.started:
            raise RuntimeError("Kernel is not started")
        task.status = TaskStatus.READY
        self.tasks.add(task, task.task_id)
        self.events.publish(
            Event(type="task.created", source="kernel", task_id=task.task_id,
                  actor_id=task.agent_id, payload={"input": task.input})
        )
        return task

    async def run_task_async(self, task_id) -> Task:
        """Run a task through the injected AgentRuntime when configured."""
        if not self.started:
            raise RuntimeError("Kernel is not started")
        task = self.tasks.get(task_id)
        if task is None:
            raise KeyError(f"Unknown task: {task_id}")
        task.status = TaskStatus.RUNNING
        task.started_at = utc_now()
        self.events.publish(Event(type="task.started", source="kernel", task_id=task.task_id))

        if self.agent_runtime is None:
            task.status = TaskStatus.COMPLETED
            task.completed_at = utc_now()
            task.result = "Task accepted by Kernel V0; execution runtime not installed yet."
            self.events.publish(Event(type="task.completed", source="kernel", task_id=task.task_id))
            return task

        result = await self.agent_runtime.run(task.input, task_id=task.task_id, agent_id=task.agent_id)
        task.completed_at = utc_now()
        if result.success:
            task.status = TaskStatus.COMPLETED
            task.result = result.output
            self.events.publish(Event(type="task.completed", source="kernel", task_id=task.task_id))
        else:
            task.status = TaskStatus.FAILED
            task.result = result.error
            self.events.publish(
                Event(type="task.failed", source="kernel", task_id=task.task_id,
                      payload={"error": result.error, "steps": result.steps})
            )
        return task

    def run_task(self, task_id) -> Task:
        """Synchronous compatibility wrapper around the async execution path."""
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(self.run_task_async(task_id))
        raise RuntimeError("Kernel.run_task() cannot run inside an event loop; use run_task_async()")
