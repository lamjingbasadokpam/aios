"""Environment contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class EnvironmentLimits:
    max_runtime_seconds: float = 300.0
    max_processes: int = 8
    max_output_bytes: int = 1_000_000
    allow_network: bool = False
    workspace_root: str | None = None


@dataclass(slots=True)
class Environment:
    name: str
    environment_id: UUID = field(default_factory=uuid4)
    capabilities: frozenset[str] = frozenset()
    limits: EnvironmentLimits = field(default_factory=EnvironmentLimits)
    status: str = "ready"
    metadata: dict = field(default_factory=dict)
