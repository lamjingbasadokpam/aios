"""Portable sandbox policy contracts; OS-specific enforcement is an adapter."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ResourceLimits:
    max_runtime_seconds: float = 300.0
    max_output_bytes: int = 1_000_000
    max_memory_mb: int | None = 512
    max_cpu_seconds: float | None = 120.0


@dataclass(frozen=True, slots=True)
class SandboxSpec:
    workspace: Path
    read_paths: tuple[Path, ...] = ()
    write_paths: tuple[Path, ...] = ()
    network: bool = False
    environment: dict[str, str] = field(default_factory=dict)
    limits: ResourceLimits = field(default_factory=ResourceLimits)

    def can_read(self, path: Path) -> bool:
        target = path.resolve()
        return any(target == root.resolve() or root.resolve() in target.parents for root in self.read_paths)

    def can_write(self, path: Path) -> bool:
        target = path.resolve()
        return any(target == root.resolve() or root.resolve() in target.parents for root in self.write_paths)
