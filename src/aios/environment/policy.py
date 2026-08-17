"""Central policy decision point for AIOS execution."""

from __future__ import annotations

from dataclasses import dataclass

from aios.tools.contracts import Tool

from .contracts import Environment


@dataclass(frozen=True, slots=True)
class Policy:
    allowed_capabilities: frozenset[str] = frozenset()
    denied_tools: frozenset[str] = frozenset()
    require_approval_for_risk: frozenset[str] = frozenset({"high", "critical"})


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    allowed: bool
    reason: str
    requires_approval: bool = False


class PolicyEngine:
    def __init__(self, policy: Policy | None = None) -> None:
        self.policy = policy or Policy()

    def evaluate(self, tool: Tool, environment: Environment) -> PolicyDecision:
        if tool.tool_id in self.policy.denied_tools:
            return PolicyDecision(False, "Tool explicitly denied by policy")

        granted = self.policy.allowed_capabilities | environment.capabilities
        missing = tool.required_capabilities - granted
        if missing:
            return PolicyDecision(
                False,
                f"Policy does not grant capabilities: {', '.join(sorted(missing))}",
            )

        if tool.network_required and not environment.limits.allow_network:
            return PolicyDecision(False, "Network access is disabled for this environment")

        if tool.risk_level in self.policy.require_approval_for_risk:
            return PolicyDecision(True, "Allowed after approval", requires_approval=True)

        return PolicyDecision(True, "Allowed")
