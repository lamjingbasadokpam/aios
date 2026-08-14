"""Agent lifecycle controller."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from .record import AgentRecord
from .registry import AgentRegistry
from aios.process.manager import AgentProcessManager, ProcessState


@dataclass(frozen=True, slots=True)
class LifecycleResult:
    agent_id: UUID
    state: ProcessState
    pid: int | None = None
    error: str | None = None


class AgentLifecycleController:
    """Coordinates registry state and process lifecycle without owning OS APIs."""

    def __init__(self, registry: AgentRegistry, processes: AgentProcessManager) -> None:
        self.registry = registry
        self.processes = processes

    def register(self, record: AgentRecord) -> AgentRecord:
        self.registry.register_record(record)
        self.processes.register(record.agent_id)
        return record

    def start(self, agent_id: UUID, *, pid: int, endpoint: str | None = None) -> LifecycleResult:
        record = self.registry.get_record(agent_id)
        if not record.identity.enabled:
            raise RuntimeError(f"Agent is disabled: {agent_id}")
        process = self.processes.get(agent_id)
        if process.state == ProcessState.RUNNING:
            return LifecycleResult(agent_id, process.state, process.pid)
        self.processes.mark_starting(agent_id)
        self.processes.mark_running(agent_id, pid, endpoint)
        return LifecycleResult(agent_id, ProcessState.RUNNING, pid)

    def stop(self, agent_id: UUID) -> LifecycleResult:
        process = self.processes.get(agent_id)
        if process.state == ProcessState.STOPPED:
            return LifecycleResult(agent_id, process.state)
        process.state = ProcessState.STOPPING
        self.processes.mark_stopped(agent_id)
        return LifecycleResult(agent_id, ProcessState.STOPPED)

    def fail(self, agent_id: UUID, error: str) -> LifecycleResult:
        process = self.processes.mark_failed(agent_id, error)
        return LifecycleResult(agent_id, process.state, process.pid, error)

    def status(self, agent_id: UUID) -> LifecycleResult:
        process = self.processes.get(agent_id)
        return LifecycleResult(agent_id, process.state, process.pid, process.last_error)

    def restart(self, agent_id: UUID, *, pid: int, endpoint: str | None = None) -> LifecycleResult:
        self.stop(agent_id)
        return self.start(agent_id, pid=pid, endpoint=endpoint)
