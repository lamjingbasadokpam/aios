"""Windows-native runtime adapter boundary for AIOS.

The core runtime stays platform-neutral; this adapter owns Windows-specific
process and IPC integration. V0 provides capability detection and command
construction only. Privileged isolation must be implemented by a dedicated
OS adapter rather than simulated in Python.
"""

from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class WindowsRuntimeCapabilities:
    windows: bool
    python: str | None
    powershell: str | None
    cmd: str | None


class WindowsRuntime:
    """Detects the Windows execution surface without spawning processes."""

    def capabilities(self) -> WindowsRuntimeCapabilities:
        return WindowsRuntimeCapabilities(
            windows=os.name == "nt",
            python=shutil.which("python"),
            powershell=shutil.which("powershell") or shutil.which("pwsh"),
            cmd=shutil.which("cmd"),
        )

    @staticmethod
    def validate_working_directory(path: str | Path) -> Path:
        directory = Path(path).resolve()
        if not directory.is_dir():
            raise NotADirectoryError(directory)
        return directory

    @staticmethod
    def command(program: str, *args: str) -> list[str]:
        return [program, *args]
