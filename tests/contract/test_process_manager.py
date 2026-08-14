from uuid import uuid4

from aios.process import AgentProcessManager, ProcessState


def test_process_lifecycle() -> None:
    agent_id = uuid4()
    manager = AgentProcessManager()
    manager.register(agent_id)
    assert manager.get(agent_id).state == ProcessState.STOPPED
    manager.mark_starting(agent_id)
    manager.mark_running(agent_id, 1234, "ipc://agent")
    record = manager.get(agent_id)
    assert record.state == ProcessState.RUNNING
    assert record.pid == 1234
    assert record.endpoint == "ipc://agent"
    manager.mark_stopped(agent_id)
    assert manager.get(agent_id).state == ProcessState.STOPPED


def test_failed_process_increments_restart_count() -> None:
    agent_id = uuid4()
    manager = AgentProcessManager()
    manager.register(agent_id)
    record = manager.mark_failed(agent_id, "crashed")
    assert record.state == ProcessState.FAILED
    assert record.restart_count == 1
    assert record.last_error == "crashed"
