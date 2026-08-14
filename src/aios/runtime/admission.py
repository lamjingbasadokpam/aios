"""Runtime admission gate combining policy, budget, and run state."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .budget import BudgetDecision, BudgetPolicy, ResourceUsage
from .control import InMemoryRuntimeController, RunState
from .policy import Decision, Policy, PolicyDecision, PolicyRequest


class AdmissionDecision(str, Enum):
    ALLOW = "allow"
    DENY = "deny"


@dataclass(frozen=True, slots=True)
class AdmissionResult:
    decision: AdmissionDecision
    reason: str
    policy: PolicyDecision | None = None


class AdmissionController:
    """Fail-closed gate before capability execution."""

    def __init__(self, policy: Policy, budget: BudgetPolicy, controller: InMemoryRuntimeController) -> None:
        self.policy = policy
        self.budget = budget
        self.controller = controller

    async def admit(self, request: PolicyRequest, usage: ResourceUsage) -> AdmissionResult:
        run = await self.controller.inspect(request.run_id)
        if run is None:
            return AdmissionResult(AdmissionDecision.DENY, "unknown run")
        if run.state != RunState.RUNNING:
            return AdmissionResult(AdmissionDecision.DENY, f"run is {run.state.value}")

        policy_result = await self.policy.evaluate(request)
        if policy_result.decision != Decision.ALLOW:
            return AdmissionResult(AdmissionDecision.DENY, policy_result.reason, policy_result)

        budget_result = self.budget.evaluate(usage)
        if budget_result.decision != BudgetDecision.ALLOW:
            return AdmissionResult(AdmissionDecision.DENY, budget_result.reason, policy_result)

        return AdmissionResult(AdmissionDecision.ALLOW, "admitted", policy_result)
