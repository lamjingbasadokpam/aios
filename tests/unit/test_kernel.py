from aios.kernel import Agent, Event, Kernel, Task


def test_kernel_lifecycle_and_events() -> None:
    kernel = Kernel()
    kernel.start()

    agent = kernel.register_agent(Agent(name="test-agent"))
    task = kernel.create_task(Task(input="hello"))
    result = kernel.run_task(task.task_id)

    assert kernel.started is True
    assert agent.name == "test-agent"
    assert result.status.value == "completed"
    assert [event.type for event in kernel.events.history()] == [
        "kernel.started",
        "agent.created",
        "task.created",
        "task.started",
        "task.completed",
    ]


def test_event_subscription() -> None:
    kernel = Kernel()
    received: list[Event] = []
    kernel.events.subscribe("task.created", received.append)
    kernel.start()
    kernel.create_task(Task(input="hello"))

    assert len(received) == 1
    assert received[0].type == "task.created"
