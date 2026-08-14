"""Resource budgets and admission decisions for AIOS runs."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class BudgetDecision(str, Enum):
    ALLOW = "allow"
    DENY = "deny"


@dataclass(frozen=True, slots=True)
class ResourceBudget:
    max_tokens: int | None = None
    max_runtime_seconds: float | None = None
    max_tool_calls: int | None = None
    max_retries: int | None = None
    max_cost: float | None = None


@dataclass(frozen=True, slots=True)
class ResourceUsage:
    tokens: int = 0
    runtime_seconds: float = 0.0
    tool_calls: int = 0
    retries: int = 0
    cost: float = 0.0


@dataclass(frozen=True, slots=True)
class BudgetResult:
    decision: BudgetDecision
    reason: str


class BudgetPolicy:
    """Deterministic fail-closed budget evaluator."""

    def __init__(self, budget: ResourceBudget) -> None:
        self.budget = budget

    def evaluate(self, usage: ResourceUsage) -> BudgetResult:
        checks = (
            (self.budget.max_tokens, usage.tokens, "token budget"),
            (self.budget.max_runtime_seconds, usage.runtime_seconds, "runtime budget"),
            (self.budget.max_tool_calls, usage.tool_calls, "tool-call budget"),
            (self.budget.max_retries, usage.retries, "retry budget"),
            (self.budget.max_cost, usage.cost, "cost budget"),
        )
        for limit, value, label in checks:
            if limit is not None and value > limit:
                return BudgetResult(BudgetDecision.DENY, f"{label} exceeded")
        return BudgetResult(BudgetDecision.ALLOW, "within configured budgets")
