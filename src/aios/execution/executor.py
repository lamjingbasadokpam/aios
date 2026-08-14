"""Bounded subprocess execution.

This V0 executor is intentionally conservative: callers must provide an
explicit executable allowlist and a working directory. It does not claim OS-
level sandboxing; stronger isolation belongs to a later backend.
"""

from __future__ import annotations

import asyncio
import os
from pathlib import Path

from .contracts import ExecutionRequest, ExecutionResult


class ExecutionDenied(PermissionError):
    """Raised when process execution violates the executor policy."""


class ProcessExecutor:
    def __init__(self, allowed_executables: frozenset[str], workspace_root: Path,
                 max_timeout_seconds: float = 300.0, max_output_bytes: int = 1_000_000) -> None:
        self.allowed_executables = allowed_executables
        self.workspace_root = workspace_root.resolve()
        self.max_timeout_seconds = max_timeout_seconds
        self.max_output_bytes = max_output_bytes

    def _resolve_workdir(self, requested: str | None) -> Path:
        root = self.workspace_root
        candidate = (root / requested).resolve() if requested else root
        if candidate != root and root not in candidate.parents:
            raise ExecutionDenied("Working directory escapes the execution workspace")
        if not candidate.is_dir():
            raise ExecutionDenied("Working directory does not exist")
        return candidate

    async def run(self, request: ExecutionRequest) -> ExecutionResult:
        if request.executable not in self.allowed_executables:
            raise ExecutionDenied(f"Executable is not allowlisted: {request.executable}")
        if request.timeout_seconds <= 0 or request.timeout_seconds > self.max_timeout_seconds:
            raise ExecutionDenied("Requested timeout exceeds execution policy")
        if request.max_output_bytes <= 0 or request.max_output_bytes > self.max_output_bytes:
            raise ExecutionDenied("Requested output limit exceeds execution policy")

        cwd = self._resolve_workdir(request.working_directory)
        env = os.environ.copy()
        env.update(request.environment)

        process = await asyncio.create_subprocess_exec(
            request.executable,
            *request.arguments,
            cwd=str(cwd),
            env=env,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        try:
            stdout, stderr = await asyncio.wait_for(process.communicate(), request.timeout_seconds)
        except asyncio.TimeoutError:
            process.kill()
            await process.wait()
            return ExecutionResult(
                success=False,
                exit_code=None,
                stdout="",
                stderr="",
                timed_out=True,
                error="Process timed out",
                execution_id=request.execution_id,
            )

        stdout = stdout[: request.max_output_bytes]
        stderr = stderr[: request.max_output_bytes]
        code = process.returncode
        return ExecutionResult(
            success=code == 0,
            exit_code=code,
            stdout=stdout.decode("utf-8", errors="replace"),
            stderr=stderr.decode("utf-8", errors="replace"),
            execution_id=request.execution_id,
        )
