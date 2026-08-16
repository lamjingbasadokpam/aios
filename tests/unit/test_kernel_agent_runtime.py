from dataclasses import dataclass

from aios.kernel import Agent, Kernel, Task
from aios.runtime import RuntimeResult


@dataclass
class FakeAgentRuntime:
    result: RuntimeResult
    calls: list[str]

    async def run(self, task: str, **kwargs) -> RuntimeResult:
        self.calls.append(task)
        return self.result


def test_kernel_executes_task_through_agent_runtime() -> None:
    runtime = FakeAgentRuntime(RuntimeResult(True, output="hello from runtime", steps=1), [])
    kernel = Kernel(agent_runtime=runtime)
    kernel.start()
    agent = kernel.register_agent(Agent(name="runtime-agent"))
    task = kernel.create_task(Task(input="say hello", agent_id=agent.agent_id))

    result = kernel.run_task(task.task_id)

    assert result.status.value == "completed"
    assert result.result == "hello from runtime"
    assert runtime.calls == ["say hello"]
    assert [event.type for event in kernel.events.history()] == [
        "kernel.started",
        "agent.created",
        "task.created",
        "task.started",
        "task.completed",
    ]


def test_kernel_records_agent_runtime_failure() -> None:
    runtime = FakeAgentRuntime(RuntimeResult(False, error="model unavailable", steps=1), [])
    kernel = Kernel(agent_runtime=runtime)
    kernel.start()
    agent = kernel.register_agent(Agent(name="runtime-agent"))
    task = kernel.create_task(Task(input="fail", agent_id=agent.agent_id))

    result = kernel.run_task(task.task_id)

    assert result.status.value == "failed"
    assert result.result == "model unavailable"
    assert runtime.calls == ["fail"]
    assert [event.type for event in kernel.events.history()] == [
        "kernel.started",
        "agent.created",
        "task.created",
        "task.started",
        "task.failed",
    ]
