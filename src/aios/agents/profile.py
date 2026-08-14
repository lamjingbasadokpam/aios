"""Declarative execution profile for an AIOS agent."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from aios.runtime.resources import ResourceLimits


@dataclass(frozen=True, slots=True)
class AgentExecutionProfile:
    """Single declarative contract used to assemble an agent worker."""

    agent_id: str
    model: str
    sandbox_profile: str
    resources: ResourceLimits = field(default_factory=ResourceLimits)
    network_allowed: bool = False
    tools: tuple[str, ...] = ()
    transport: str = "in_process"
    environment: dict[str, str] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.agent_id.strip():
            raise ValueError("agent_id is required")
        if not self.model.strip():
            raise ValueError("model is required")
        if not self.sandbox_profile.strip():
            raise ValueError("sandbox_profile is required")
        if not self.transport.strip():
            raise ValueError("transport is required")

    def as_dict(self) -> dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "model": self.model,
            "sandbox_profile": self.sandbox_profile,
            "resources": {
                "max_processes": self.resources.max_processes,
                "memory_bytes": self.resources.memory_bytes,
                "cpu_time_seconds": self.resources.cpu_time_seconds,
            },
            "network_allowed": self.network_allowed,
            "tools": list(self.tools),
            "transport": self.transport,
            "environment": dict(self.environment),
            "metadata": dict(self.metadata),
        }
