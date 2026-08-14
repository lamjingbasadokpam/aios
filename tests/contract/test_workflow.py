import pytest

from aios.agent.execution import PlanExecutor, StepStatus
from aios.agent.planning import Plan, PlanStep
from aios.agent.workflow import Workflow, WorkflowRunner, WorkflowState, WorkflowStatus


class Executor:
    async def execute(self, step):
        return step.description


@pytest.mark.asyncio
async def test_workflow_runner_tracks_state() -> None:
    plan = Plan("goal", (PlanStep("first"), PlanStep("second")))
    workflow = Workflow(plan)
    state = await WorkflowRunner(PlanExecutor(Executor())).run(workflow)
    assert state.status == WorkflowStatus.SUCCEEDED
    assert len(state.completed_steps) == 2
    assert all(result.status == StepStatus.SUCCEEDED for result in state.results)


@pytest.mark.asyncio
async def test_completed_workflow_is_idempotent() -> None:
    plan = Plan("goal", (PlanStep("first"),))
    workflow = Workflow(plan)
    runner = WorkflowRunner(PlanExecutor(Executor()))
    state = WorkflowState(workflow.workflow_id, WorkflowStatus.SUCCEEDED)
    result = await runner.run(workflow, state)
    assert result is state
