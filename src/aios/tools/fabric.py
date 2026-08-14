"""Provider-neutral tool execution fabric for AIOS agents."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass(frozen=True, slots=True)
class ToolRequest:
    tool: str
    arguments: dict[str, Any] = field(default_factory=dict)
    request_id: str | None = None


@dataclass(frozen=True, slots=True)
class ToolResponse:
    tool: str
    success: bool
    result: Any = None
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class ToolAdapter(Protocol):
    async def execute(self, request: ToolRequest) -> ToolResponse: ...


class ToolFabric:
    """Explicitly registered tool boundary; policy stays outside adapters."""

    def __init__(self) -> None:
        self._tools: dict[str, ToolAdapter] = {}

    def register(self, name: str, adapter: ToolAdapter) -> None:
        if not name.strip():
            raise ValueError("tool name is required")
        if name in self._tools:
            raise ValueError(f"Tool already registered: {name}")
        self._tools[name] = adapter

    def list_tools(self) -> tuple[str, ...]:
        return tuple(sorted(self._tools))

    async def execute(self, request: ToolRequest) -> ToolResponse:
        try:
            adapter = self._tools[request.tool]
        except KeyError as exc:
            raise LookupError(f"No tool registered: {request.tool}") from exc
        return await adapter.execute(request)
