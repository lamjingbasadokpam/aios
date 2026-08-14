"""Stable contracts for executable capabilities."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class Tool:
    tool_id: str
    name: str
    description: str
    input_schema: dict[str, Any] = field(default_factory=dict)
    output_schema: dict[str, Any] = field(default_factory=dict)
    required_capabilities: frozenset[str] = frozenset()
    risk_level: str = "low"
    network_required: bool = False
    filesystem_required: bool = False
    version: str = "0.1.0"
    health: str = "healthy"


@dataclass(frozen=True, slots=True)
class ToolContext:
    task_id: UUID | None = None
    agent_id: UUID | None = None
    environment_id: str | None = None
    granted_capabilities: frozenset[str] = frozenset()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ToolResult:
    success: bool
    output: Any = None
    error: str | None = None
    tool_id: str | None = None
    invocation_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)


class ToolHandler(Protocol):
    async def __call__(self, arguments: dict[str, Any], context: ToolContext) -> ToolResult: ...
