from pathlib import Path
from uuid import uuid4

from aios.agents.identity import AgentIdentity
from aios.agents.launcher import AgentLauncher
from aios.agents.lifecycle import AgentLifecycleController
from aios.agents.profile import AgentExecutionProfile
from aios.agents.record import AgentRecord
from aios.agents.registry import AgentRegistry
from aios.process.manager import AgentProcessManager, ProcessState
from aios.runtime.process import ProcessHandle


class FakeLauncher:
    def spawn(self, command, *, cwd, env=None):
        self.command = command
        self.cwd = cwd
        self.env = env
        return object(), ProcessHandle(4242, tuple(command))


def test_launcher_builds_and_registers_process(tmp_path: Path) -> None:
    agent_id = uuid4()
    record = AgentRecord(
        AgentIdentity("coder", "developer", "local/default", "coder", "restricted", agent_id=agent_id),
        AgentExecutionProfile(str(agent_id), "local/default", "restricted", environment={"AIOS_AGENT": "coder"}),
    )
    registry = AgentRegistry()
    processes = AgentProcessManager()
    lifecycle = AgentLifecycleController(registry, processes)
    lifecycle.register(record)
    fake = FakeLauncher()
    launcher = AgentLauncher(lifecycle, fake)

    result, handle = launcher.launch(record, command=["python", "worker.py"], cwd=tmp_path, endpoint="pipe://coder")
    assert result.state == ProcessState.RUNNING
    assert handle.pid == 4242
    assert fake.env == {"AIOS_AGENT": "coder"}
    assert lifecycle.status(agent_id).pid == 4242
