from aios.agents.profile import AgentExecutionProfile
from aios.runtime.resources import ResourceLimits


def test_execution_profile_serializes_runtime_contract() -> None:
    profile = AgentExecutionProfile(
        agent_id="coder",
        model="local/default",
        sandbox_profile="restricted",
        resources=ResourceLimits(max_processes=2, memory_bytes=4 * 1024**3, cpu_time_seconds=60),
        tools=("filesystem", "terminal"),
        transport="ipc",
    )
    data = profile.as_dict()
    assert data["agent_id"] == "coder"
    assert data["resources"]["memory_bytes"] == 4 * 1024**3
    assert data["tools"] == ["filesystem", "terminal"]
    assert data["transport"] == "ipc"
