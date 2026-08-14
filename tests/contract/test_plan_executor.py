import pytest

from aios.agent.execution import PlanExecutor, StepStatus
from aios.agent.planning import Plan, PlanStep


class Executor:
    def __init__(self):
        self.calls = []

    async def execute(self, step):
        self.calls.append(step.description)
        return f"done:{step.description}"


@pytest.mark.asyncio
async def test_plan_executor_respects_dependencies() -> None:
    executor = Executor()
    first = PlanStep("first")
    second = PlanStep("second", depends_on=(first.step_id,))
    results = await PlanExecutor(executor).execute(Plan("goal", (first, second)))
    assert [r.status for r in results] == [StepStatus.SUCCEEDED, StepStatus.SUCCEEDED]
    assert executor.calls == ["first", "second"]


@pytest.mark.asyncio
async def test_plan_executor_retries_bounded_failures() -> None:
    class Failing:
        def __init__(self):
            self.calls = 0

        async def execute(self, step):
            self.calls += 1
            raise RuntimeError("boom")

    failing = Failing()
    results = await PlanExecutor(failing, max_retries=2).execute(Plan("goal", (PlanStep("fail"),)))
    assert results[0].status == StepStatus.FAILED
    assert results[0].attempts == 3
    assert failing.calls == 3
