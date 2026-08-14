"""Security gateway between agents and executable tools."""

from __future__ import annotations

from aios.environment import Environment, PolicyEngine

from .contracts import ToolContext, ToolResult
from .registry import ToolRegistry


class ToolDenied(PermissionError):
    """Raised when a capability or environment policy blocks invocation."""


class ToolApprovalRequired(PermissionError):
    """Raised when policy requires an approval checkpoint."""


class ToolGateway:
    def __init__(self, registry: ToolRegistry, policy_engine: PolicyEngine | None = None) -> None:
        self.registry = registry
        self.policy_engine = policy_engine or PolicyEngine()

    async def invoke(self, tool_id: str, arguments: dict, context: ToolContext,
                     environment: Environment | None = None,
                     approval_granted: bool = False) -> ToolResult:
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

        env = environment or Environment(name="default", capabilities=context.granted_capabilities)
        decision = self.policy_engine.evaluate(tool, env)
        if not decision.allowed:
            raise ToolDenied(decision.reason)
        if decision.requires_approval and not approval_granted:
            raise ToolApprovalRequired(decision.reason)

        handler = self.registry.handler(tool_id)
        if handler is None:
            raise RuntimeError(f"No handler registered for tool: {tool_id}")
        return await handler(arguments, context)
