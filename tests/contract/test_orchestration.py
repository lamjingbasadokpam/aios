import asyncio

from aios.orchestration import OrchestrationTask, Orchestrator, TaskGraph, TaskState


def test_orchestrator_respects_dependencies() -> None:
    order = []
    graph = TaskGraph()

    async def first(ctx):
        order.append("first")
        return "A"

    async def second(ctx):
        order.append("second")
        assert any(value == "A" for value in ctx.values())
        return "B"

    a = OrchestrationTask("first", first)
    b = OrchestrationTask("second", second, dependencies=(a.task_id,))
    graph.add(a)
    graph.add(b)

    results = asyncio.run(Orchestrator(graph).run())
    assert results[a.task_id].state == TaskState.SUCCEEDED
    assert results[b.task_id].state == TaskState.SUCCEEDED
    assert order == ["first", "second"]


def test_orchestrator_retries_failed_task() -> None:
    graph = TaskGraph()
    attempts = 0

    async def flaky(ctx):
        nonlocal attempts
        attempts += 1
        if attempts < 2:
            raise RuntimeError("temporary")
        return "ok"

    task = OrchestrationTask("flaky", flaky, retry_limit=1)
    graph.add(task)
    result = asyncio.run(Orchestrator(graph).run())[task.task_id]
    assert result.state == TaskState.SUCCEEDED
    assert result.attempts == 2


def test_graph_rejects_cycle() -> None:
    graph = TaskGraph()
    a = OrchestrationTask("a", lambda ctx: asyncio.sleep(0))
    b = OrchestrationTask("b", lambda ctx: asyncio.sleep(0), dependencies=(a.task_id,))
    graph.add(a)
    graph.add(b)
    # Replacing the immutable task is intentionally avoided; a missing dependency
    # is enough to verify graph validation rejects invalid topology.
    graph._tasks[a.task_id] = OrchestrationTask("a", a.handler, dependencies=(b.task_id,))
    try:
        graph.validate()
    except ValueError as exc:
        assert "cycle" in str(exc)
    else:
        raise AssertionError("cycle was not rejected")
