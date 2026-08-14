"""AIOS Kernel V0 orchestration of core in-memory services."""

from __future__ import annotations

from .events import Event, EventBus
from .models import Agent, AgentStatus, Task, TaskStatus, utc_now
from .registry import Registry
from .resources import ResourceRegistry


class Kernel:
    def __init__(self) -> None:
        self.agents: Registry[Agent] = Registry()
        self.tasks: Registry[Task] = Registry()
        self.resources = ResourceRegistry()
        self.events = EventBus()
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

    def run_task(self, task_id) -> Task:
        if not self.started:
            raise RuntimeError("Kernel is not started")
        task = self.tasks.get(task_id)
        if task is None:
            raise KeyError(f"Unknown task: {task_id}")
        task.status = TaskStatus.RUNNING
        task.started_at = utc_now()
        self.events.publish(Event(type="task.started", source="kernel", task_id=task.task_id))
        # Kernel V0 deliberately has no model/agent execution yet.
        task.status = TaskStatus.COMPLETED
        task.completed_at = utc_now()
        task.result = "Task accepted by Kernel V0; execution runtime not installed yet."
        self.events.publish(Event(type="task.completed", source="kernel", task_id=task.task_id))
        return task
