import pytest

from aios.agent.checkpoint import InMemoryCheckpointStore
from aios.agent.execution import StepResult, StepStatus
from aios.agent.workflow import WorkflowState, WorkflowStatus


@pytest.mark.asyncio
async def test_checkpoint_round_trip() -> None:
    store = InMemoryCheckpointStore()
    state = WorkflowState("wf-1", WorkflowStatus.RUNNING)
    state.completed_steps.add("step-1")
    state.results.append(StepResult("step-1", StepStatus.SUCCEEDED, output="ok"))
    await store.save(state)
    restored = await store.load("wf-1")
    assert restored is not None
    assert restored.workflow_id == state.workflow_id
    assert restored.status == WorkflowStatus.RUNNING
    assert restored.completed_steps == {"step-1"}
    assert restored.results[0].output == "ok"


@pytest.mark.asyncio
async def test_missing_checkpoint_returns_none() -> None:
    assert await InMemoryCheckpointStore().load("missing") is None
