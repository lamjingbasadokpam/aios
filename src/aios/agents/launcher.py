"""Agent launch orchestration between profiles and OS runtime adapters."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from .lifecycle import AgentLifecycleController, LifecycleResult
from .record import AgentRecord
from aios.runtime.process import ProcessHandle


class ProcessLauncher(Protocol):
    def spawn(self, command: list[str], *, cwd: str | Path, env: dict[str, str] | None = None): ...


@dataclass(frozen=True, slots=True)
class LaunchRequest:
    command: tuple[str, ...]
    cwd: Path
    environment: dict[str, str]


class AgentLauncher:
    """Turns an agent record into a process and reports it to lifecycle state."""

    def __init__(self, lifecycle: AgentLifecycleController, process_launcher: ProcessLauncher) -> None:
        self.lifecycle = lifecycle
        self.process_launcher = process_launcher

    def build_request(self, record: AgentRecord, *, command: list[str], cwd: str | Path) -> LaunchRequest:
        if not command:
            raise ValueError("agent launch command is required")
        directory = Path(cwd).resolve()
        if not directory.is_dir():
            raise NotADirectoryError(directory)
        return LaunchRequest(tuple(command), directory, dict(record.profile.environment))

    def launch(self, record: AgentRecord, *, command: list[str], cwd: str | Path, endpoint: str | None = None) -> tuple[LifecycleResult, ProcessHandle]:
        request = self.build_request(record, command=command, cwd=cwd)
        process, handle = self.process_launcher.spawn(
            list(request.command), cwd=request.cwd, env=request.environment or None
        )
        result = self.lifecycle.start(record.agent_id, pid=handle.pid, endpoint=endpoint)
        return result, handle
