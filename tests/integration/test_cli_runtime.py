import asyncio

from aios.cli.main import build_kernel
from aios.kernel import Task


def test_cli_kernel_factory_executes_task_through_runtime() -> None:
    async def scenario():
        kernel = build_kernel()
        kernel.start()
        task = kernel.create_task(Task(input="Say hello"))
        return await kernel.run_task_async(task.task_id)

    task = asyncio.run(scenario())

    assert task.status.value == "completed"
    assert task.result == "[mock-local] Say hello"
    assert [event.type for event in kernel.events.history()] == [
        "kernel.started",
        "task.created",
        "task.started",
        "task.completed",
    ]
