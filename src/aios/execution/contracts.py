"""Normalized process execution contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class ExecutionRequest:
    executable: str
    arguments: tuple[str, ...] = ()
    working_directory: str | None = None
    environment: dict[str, str] = field(default_factory=dict)
    timeout_seconds: float = 30.0
    max_output_bytes: int = 1_000_000
    execution_id: UUID = field(default_factory=uuid4)


@dataclass(frozen=True, slots=True)
class ExecutionResult:
    success: bool
    exit_code: int | None
    stdout: str
    stderr: str
    timed_out: bool = False
    error: str | None = None
    execution_id: UUID | None = None
