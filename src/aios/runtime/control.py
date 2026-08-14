"""Runtime control-plane contracts for managing AIOS executions."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Protocol


class RunState(str, Enum):
    CREATED = "created"
    RUNNING = "running"
    PAUSED = "paused"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(slots=True)
class RunHandle:
    run_id: str
    state: RunState = RunState.CREATED
    metadata: dict[str, str] = field(default_factory=dict)


class RuntimeController(Protocol):
    async def pause(self, run_id: str) -> RunHandle: ...
    async def resume(self, run_id: str) -> RunHandle: ...
    async def cancel(self, run_id: str) -> RunHandle: ...
    async def inspect(self, run_id: str) -> RunHandle | None: ...


class InMemoryRuntimeController:
    """Deterministic local control-plane state machine."""

    def __init__(self) -> None:
        self._runs: dict[str, RunHandle] = {}

    def register(self, run_id: str) -> RunHandle:
        handle = RunHandle(run_id)
        self._runs[run_id] = handle
        return handle

    async def pause(self, run_id: str) -> RunHandle:
        handle = self._require(run_id)
        if handle.state != RunState.RUNNING:
            raise ValueError("only running runs can be paused")
        handle.state = RunState.PAUSED
        return handle

    async def resume(self, run_id: str) -> RunHandle:
        handle = self._require(run_id)
        if handle.state != RunState.PAUSED:
            raise ValueError("only paused runs can be resumed")
        handle.state = RunState.RUNNING
        return handle

    async def cancel(self, run_id: str) -> RunHandle:
        handle = self._require(run_id)
        if handle.state in {RunState.COMPLETED, RunState.CANCELLED}:
            raise ValueError("run is already terminal")
        handle.state = RunState.CANCELLED
        return handle

    async def inspect(self, run_id: str) -> RunHandle | None:
        return self._runs.get(run_id)

    def _require(self, run_id: str) -> RunHandle:
        try:
            return self._runs[run_id]
        except KeyError as exc:
            raise KeyError(f"unknown run: {run_id}") from exc
