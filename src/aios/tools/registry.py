"""Tool discovery registry."""

from __future__ import annotations

from .contracts import Tool, ToolHandler


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}
        self._handlers: dict[str, ToolHandler] = {}

    def register(self, tool: Tool, handler: ToolHandler) -> None:
        if tool.tool_id in self._tools:
            raise ValueError(f"Tool already registered: {tool.tool_id}")
        self._tools[tool.tool_id] = tool
        self._handlers[tool.tool_id] = handler

    def get(self, tool_id: str) -> Tool | None:
        return self._tools.get(tool_id)

    def handler(self, tool_id: str) -> ToolHandler | None:
        return self._handlers.get(tool_id)

    def list(self) -> list[Tool]:
        return list(self._tools.values())
