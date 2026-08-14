import pytest

from aios.runtime.admission import AdmissionController, AdmissionDecision
from aios.runtime.budget import BudgetPolicy, ResourceBudget, ResourceUsage
from aios.runtime.control import InMemoryRuntimeController, RunState
from aios.runtime.policy import AllowListPolicy, PolicyRequest


@pytest.mark.asyncio
async def test_admission_requires_running_run_and_allows_valid_request() -> None:
    controller = InMemoryRuntimeController()
    run = controller.register("run-1")
    run.state = RunState.RUNNING
    gate = AdmissionController(
        AllowListPolicy({"filesystem": {"read"}}),
        BudgetPolicy(ResourceBudget(max_tool_calls=2)),
        controller,
    )
    result = await gate.admit(PolicyRequest("run-1", "filesystem", "read"), ResourceUsage(tool_calls=1))
    assert result.decision == AdmissionDecision.ALLOW


@pytest.mark.asyncio
async def test_admission_fails_closed_on_policy_or_budget() -> None:
    controller = InMemoryRuntimeController()
    run = controller.register("run-2")
    run.state = RunState.RUNNING
    gate = AdmissionController(
        AllowListPolicy({"filesystem": {"read"}}),
        BudgetPolicy(ResourceBudget(max_tool_calls=1)),
        controller,
    )
    denied_policy = await gate.admit(PolicyRequest("run-2", "filesystem", "write"), ResourceUsage())
    denied_budget = await gate.admit(PolicyRequest("run-2", "filesystem", "read"), ResourceUsage(tool_calls=2))
    assert denied_policy.decision == AdmissionDecision.DENY
    assert denied_budget.decision == AdmissionDecision.DENY
