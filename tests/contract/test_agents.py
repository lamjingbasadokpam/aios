from uuid import uuid4

import pytest

from aios.agents import AgentIdentity, AgentRegistry


def make_agent() -> AgentIdentity:
    return AgentIdentity(
        name="Coder",
        role="software_engineer",
        model="local/default",
        memory_namespace="coder",
        sandbox_profile="dev",
        tools=("filesystem.read", "filesystem.write"),
    )


def test_registry_register_get_and_list() -> None:
    registry = AgentRegistry()
    agent = registry.register(make_agent())
    assert registry.get(agent.agent_id) == agent
    assert registry.list() == (agent,)
    assert registry.list(enabled_only=True) == (agent,)


def test_registry_prevents_duplicate_identity() -> None:
    registry = AgentRegistry()
    agent = make_agent()
    registry.register(agent)
    with pytest.raises(ValueError):
        registry.register(agent)


def test_registry_disable_and_enable() -> None:
    registry = AgentRegistry()
    agent = registry.register(make_agent())
    registry.disable(agent.agent_id)
    assert registry.list(enabled_only=True) == ()
    updated = registry.enable(agent.agent_id)
    assert updated.enabled
