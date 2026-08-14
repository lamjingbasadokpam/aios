import pytest

from aios.runtime.control import InMemoryRuntimeController, RunState


@pytest.mark.asyncio
async def test_runtime_control_pause_resume_cancel() -> None:
    controller = InMemoryRuntimeController()
    run = controller.register("run-1")
    run.state = RunState.RUNNING

    assert (await controller.pause("run-1")).state == RunState.PAUSED
    assert (await controller.resume("run-1")).state == RunState.RUNNING
    assert (await controller.cancel("run-1")).state == RunState.CANCELLED


@pytest.mark.asyncio
async def test_invalid_transition_is_rejected() -> None:
    controller = InMemoryRuntimeController()
    controller.register("run-2")
    with pytest.raises(ValueError, match="running"):
        await controller.pause("run-2")
