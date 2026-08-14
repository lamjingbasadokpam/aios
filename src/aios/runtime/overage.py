"""Runtime overage enforcement policy for AIOS resource budgets."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .budget import ResourceUsage
from .settlement import SettlementResult, SettlementStatus


class OverageAction(str, Enum):
    ALLOW = "allow"
    WARN = "warn"
    STOP = "stop"


@dataclass(frozen=True, slots=True)
class OveragePolicy:
    action: OverageAction = OverageAction.STOP
    grace_tokens: int = 0
    grace_runtime_seconds: float = 0.0
    grace_tool_calls: int = 0
    grace_retries: int = 0
    grace_cost: float = 0.0


@dataclass(frozen=True, slots=True)
class OverageDecision:
    action: OverageAction
    reason: str
    overage: ResourceUsage


class OverageGuard:
    """Turns settlement overages into an explicit runtime enforcement decision."""

    def __init__(self, policy: OveragePolicy | None = None) -> None:
        self.policy = policy or OveragePolicy()

    def evaluate(self, settlement: SettlementResult) -> OverageDecision:
        if settlement.status != SettlementStatus.OVERAGE:
            return OverageDecision(OverageAction.ALLOW, "no overage", ResourceUsage())

        over = settlement.overage
        within_grace = (
            over.tokens <= self.policy.grace_tokens
            and over.runtime_seconds <= self.policy.grace_runtime_seconds
            and over.tool_calls <= self.policy.grace_tool_calls
            and over.retries <= self.policy.grace_retries
            and over.cost <= self.policy.grace_cost
        )
        if within_grace:
            action = OverageAction.WARN
        else:
            action = self.policy.action
        return OverageDecision(action, f"resource overage detected: {action.value}", over)
