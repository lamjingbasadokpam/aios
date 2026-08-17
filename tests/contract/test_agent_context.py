import pytest
from uuid import uuid4

from aios.agent.context import AgentContextBuilder
from aios.memory.context import ContextEngine
from aios.memory.gateway import MemoryAccessContext, MemoryGateway
from aios.memory.store import MemoryStore


@pytest.mark.asyncio
async def test_agent_context_builder_retrieves_and_packs_memory() -> None:
    store = MemoryStore()
    gateway = MemoryGateway(store)
    access = MemoryAccessContext(agent_id=uuid4())
    gateway.remember(
        "AIOS is a local agent operating system",
        source="manual.md",
        context=access,
    )
    builder = AgentContextBuilder(gateway, ContextEngine(100))
    context = builder.build(
        query="local agent operating system",
        messages=[{"role": "user", "content": "hi"}],
        access=access,
    )
    assert len(context.messages) == 1
    assert context.memory.items
    assert "manual.md" in builder.as_system_context(context)


@pytest.mark.asyncio
async def test_agent_context_builder_rejects_unauthorized_memory_scope() -> None:
    store = MemoryStore()
    gateway = MemoryGateway(store)
    owner = MemoryAccessContext(agent_id=uuid4())
    attacker = MemoryAccessContext(agent_id=uuid4())
    gateway.remember(
        "private agent memory",
        source="private.md",
        context=owner,
    )
    builder = AgentContextBuilder(gateway, ContextEngine(100))

    context = builder.build(
        query="private agent memory",
        messages=[],
        access=attacker,
    )
    assert not context.memory.items
