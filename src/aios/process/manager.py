"""Portable agent process lifecycle registry."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID


class ProcessState(StrEnum):
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    FAILED = "failed"


@dataclass(slots=True)
class ProcessRecord:
    agent_id: UUID
    state: ProcessState = ProcessState.STOPPED
    pid: int | None = None
    endpoint: str | None = None
    restart_count: int = 0
    last_error: str | None = None


class AgentProcessManager:
    """Tracks process lifecycle; OS-specific spawning is deliberately an adapter."""

    def __init__(self) -> None:
        self._records: dict[UUID, ProcessRecord] = {}

    def register(self, agent_id: UUID) -> ProcessRecord:
        if agent_id in self._records:
            raise ValueError(f"Agent process already registered: {agent_id}")
        record = ProcessRecord(agent_id)
        self._records[agent_id] = record
        return record

    def get(self, agent_id: UUID) -> ProcessRecord:
        return self._records[agent_id]

    def mark_starting(self, agent_id: UUID) -> ProcessRecord:
        record = self.get(agent_id)
        record.state = ProcessState.STARTING
        record.last_error = None
        return record

    def mark_running(self, agent_id: UUID, pid: int, endpoint: str | None = None) -> ProcessRecord:
        record = self.get(agent_id)
        record.state = ProcessState.RUNNING
        record.pid = pid
        record.endpoint = endpoint
        return record

    def mark_failed(self, agent_id: UUID, error: str) -> ProcessRecord:
        record = self.get(agent_id)
        record.state = ProcessState.FAILED
        record.last_error = error
        record.restart_count += 1
        return record

    def mark_stopped(self, agent_id: UUID) -> ProcessRecord:
        record = self.get(agent_id)
        record.state = ProcessState.STOPPED
        record.pid = None
        return record
