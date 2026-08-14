"""Windows process adapter for AIOS agent workers."""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from subprocess import Popen


@dataclass(frozen=True, slots=True)
class ProcessHandle:
    pid: int
    command: tuple[str, ...]


class WindowsProcessAdapter:
    """Small OS adapter; policy and lifecycle state remain outside this class."""

    def spawn(
        self,
        command: list[str],
        *,
        cwd: str | Path,
        env: dict[str, str] | None = None,
    ) -> tuple[Popen[str], ProcessHandle]:
        if os.name != "nt":
            raise OSError("WindowsProcessAdapter requires Windows")
        process = subprocess.Popen(
            command,
            cwd=str(cwd),
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
        )
        return process, ProcessHandle(process.pid, tuple(command))

    @staticmethod
    def terminate(process: Popen[str], *, timeout: float = 5.0) -> None:
        if process.poll() is not None:
            return
        process.terminate()
        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
