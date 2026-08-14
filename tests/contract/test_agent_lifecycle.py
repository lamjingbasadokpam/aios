from uuid import uuid4

from aios.agents.identity import AgentIdentity
from aios.agents.lifecycle import AgentLifecycleController
from aios.agents.profile import AgentExecutionProfile
from aios.agents.record import AgentRecord
from aios.agents.registry import AgentRegistry
from aios.process.manager import AgentProcessManager, ProcessState


def make_record() -> AgentRecord:
    agent_id = uuid4()
    identity = AgentIdentity("coder", "developer", "local/default", "coder", "restricted", agent_id=agent_id)
    profile = AgentExecutionProfile(agent_id=str(agent_id), model="local/default", sandbox_profile="restricted")
    return AgentRecord(identity, profile)


def test_lifecycle_start_status_stop() -> None:
    registry = AgentRegistry()
    processes = AgentProcessManager()
    controller = AgentLifecycleController(registry, processes)
    record = controller.register(make_record())
    started = controller.start(record.agent_id, pid=123, endpoint="ipc://coder")
    assert started.state == ProcessState.RUNNING
    assert controller.status(record.agent_id).pid == 123
    stopped = controller.stop(record.agent_id)
    assert stopped.state == ProcessState.STOPPED


def test_disabled_agent_cannot_start() -> None:
    record = make_record()
    identity = AgentIdentity("coder", "developer", "local/default", "coder", "restricted", agent_id=record.agent_id, enabled=False)
    record = AgentRecord(identity, record.profile)
    controller = AgentLifecycleController(AgentRegistry(), AgentProcessManager())
    controller.register(record)
    import pytest
    with pytest.raises(RuntimeError):
        controller.start(record.agent_id, pid=123)
