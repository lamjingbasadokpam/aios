"""Resource-control contracts and Windows Job Object adapter boundary."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ResourceLimits:
    max_processes: int | None = None
    memory_bytes: int | None = None
    cpu_time_seconds: int | None = None

    def __post_init__(self) -> None:
        for name, value in (("max_processes", self.max_processes), ("memory_bytes", self.memory_bytes), ("cpu_time_seconds", self.cpu_time_seconds)):
            if value is not None and value <= 0:
                raise ValueError(f"{name} must be positive")


class WindowsJobObjectAdapter:
    """Capability boundary for Windows Job Objects.

    Native Job Object calls are isolated here so the core can remain portable.
    V0 tracks attachments; privileged OS enforcement belongs in this adapter.
    """

    def __init__(self, limits: ResourceLimits) -> None:
        self.limits = limits
        self._attached_pids: set[int] = set()

    @property
    def supported(self) -> bool:
        return os.name == "nt"

    def attach(self, pid: int) -> None:
        if not self.supported:
            raise OSError("Windows Job Objects require Windows")
        if pid <= 0:
            raise ValueError("pid must be positive")
        self._attached_pids.add(pid)

    def attached(self, pid: int) -> bool:
        return pid in self._attached_pids
