import pytest

from aios.agent.context import AgentContextBuilder
from aios.memory.context import ContextEngine
from aios.memory.contracts import MemoryQuery
from aios.memory.hybrid import HybridRetriever
from aios.memory.retrieval import RetrievalEngine
from aios.memory.store import MemoryStore


@pytest.mark.asyncio
async def test_agent_context_builder_retrieves_and_packs_memory() -> None:
    store = MemoryStore()
    store.remember("AIOS is a local agent operating system", source="manual.md")
    builder = AgentContextBuilder(HybridRetriever(RetrievalEngine(store)), ContextEngine(100))
    context = await builder.build(query="local agent operating system", messages=[{"role": "user", "content": "hi"}])
    assert len(context.messages) == 1
    assert context.memory.items
    assert "manual.md" in builder.as_system_context(context)
