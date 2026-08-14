import pytest

from aios.agent.planning import Plan, PlanStep, PlanValidator, StaticPlanner


@pytest.mark.asyncio
async def test_static_planner_creates_valid_plan() -> None:
    plan = await StaticPlanner().create_plan("inspect repository")
    assert plan.goal == "inspect repository"
    assert len(plan.steps) == 1
    PlanValidator.validate(plan)


def test_plan_validator_rejects_unknown_dependency() -> None:
    plan = Plan("goal", (PlanStep("step", depends_on=("missing",)),))
    with pytest.raises(ValueError, match="Unknown dependency"):
        PlanValidator.validate(plan)
