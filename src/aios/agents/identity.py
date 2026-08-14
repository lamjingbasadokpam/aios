"""Persistent identity for an AIOS agent."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class AgentIdentity:
    name: str
    role: str
    model: str
    memory_namespace: str
    sandbox_profile: str
    tools: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)
    agent_id: UUID = field(default_factory=uuid4)
    enabled: bool = True
