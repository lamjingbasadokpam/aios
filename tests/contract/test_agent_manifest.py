import pytest

from aios.agents.manifest import AgentManifestLoader, ManifestError


def test_manifest_loader_builds_profile() -> None:
    text = """
id: researcher
model:
  provider: local
  name: qwen
sandbox: restricted
resources:
  processes: 3
  memory_bytes: 4294967296
  cpu_time_seconds: 120
network: true
tools:
  - filesystem.read
  - web.search
transport:
  type: ipc
"""
    profile = AgentManifestLoader().load_text(text)
    assert profile.agent_id == "researcher"
    assert profile.model == "local/qwen"
    assert profile.resources.max_processes == 3
    assert profile.network_allowed is True
    assert profile.tools == ("filesystem.read", "web.search")
    assert profile.transport == "ipc"


def test_manifest_loader_rejects_non_mapping() -> None:
    with pytest.raises(ManifestError):
        AgentManifestLoader().from_mapping([])  # type: ignore[arg-type]
