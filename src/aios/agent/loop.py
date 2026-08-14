"""Framework-neutral agent decision and tool-calling loop."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from aios.model.gateway import ModelGateway, ModelRequest, ModelResponse
from aios.tools.fabric import ToolFabric, ToolRequest, ToolResponse


@dataclass(frozen=True, slots=True)
class AgentStep:
    kind: str
    content: str | None = None
    tool: str | None = None
    arguments: dict[str, Any] | None = None
    result: Any = None


class ToolCallParser(Protocol):
    def parse(self, response: ModelResponse) -> AgentStep: ...


class AgentLoop:
    """Runs model -> tool -> observation cycles without owning provider SDKs."""

    def __init__(self, model: ModelGateway, tools: ToolFabric, parser: ToolCallParser) -> None:
        self.model = model
        self.tools = tools
        self.parser = parser

    async def run(self, *, provider: str, model: str, messages: list[dict[str, Any]], max_steps: int = 8) -> str:
        if max_steps <= 0:
            raise ValueError("max_steps must be positive")
        history = list(messages)
        for _ in range(max_steps):
            response = await self.model.generate(provider, ModelRequest(model, tuple(history)))
            step = self.parser.parse(response)
            if step.kind == "final":
                return step.content or response.content
            if step.kind != "tool_call" or not step.tool:
                raise ValueError("parser returned an invalid agent step")
            tool_response: ToolResponse = await self.tools.execute(
                ToolRequest(step.tool, step.arguments or {})
            )
            history.append({"role": "assistant", "content": response.content})
            history.append({
                "role": "tool",
                "name": step.tool,
                "content": tool_response.result if tool_response.success else tool_response.error,
            })
        raise RuntimeError("agent loop exceeded max_steps")
