"""Security gateway between agents and executable tools."""

from __future__ import annotations

from .contracts import ToolContext, ToolResult
from .registry import ToolRegistry


class ToolDenied(PermissionError):
    """Raised when a policy/capability check blocks a tool invocation."""


class ToolGateway:
    def __init__(self, registry: ToolRegistry) -> None:
        self.registry = registry

    async def invoke(self, tool_id: str, arguments: dict, context: ToolContext) -> ToolResult:
        tool = self.registry.get(tool_id)
        if tool is None:
            raise KeyError(f"Unknown tool: {tool_id}")
        if tool.health == "unavailable":
            return ToolResult(success=False, error="Tool unavailable", tool_id=tool_id)

        missing = tool.required_capabilities - context.granted_capabilities
        if missing:
            raise ToolDenied(
                f"Tool '{tool.name}' requires capabilities: {', '.join(sorted(missing))}"
            )

        handler = self.registry.handler(tool_id)
        if handler is None:
            raise RuntimeError(f"No handler registered for tool: {tool_id}")
        return await handler(arguments, context)
