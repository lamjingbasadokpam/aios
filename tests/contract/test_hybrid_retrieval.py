import pytest

from aios.memory.contracts import MemoryQuery, MemoryRecord
from aios.memory.hybrid import HybridRetriever
from aios.memory.retrieval import RetrievalEngine
from aios.memory.store import MemoryStore
from aios.memory.vector import HashEmbedder, InMemoryVectorIndex


@pytest.mark.asyncio
async def test_hybrid_retrieval_fuses_lexical_and_vector_candidates() -> None:
    store = MemoryStore()
    first = store.remember("AIOS agent runtime architecture", source="doc")
    store.remember("unrelated database note", source="doc")
    records = [first]
    embedder = HashEmbedder(64)
    index = InMemoryVectorIndex()
    await index.upsert(records, await embedder.embed([record.content for record in records]))
    result = await HybridRetriever(RetrievalEngine(store, embedder, index)).retrieve(
        MemoryQuery("agent architecture", top_k=1)
    )
    assert result.strategy == "hybrid_rrf"
    assert result.hits[0].record.content == first.content


@pytest.mark.asyncio
async def test_hybrid_degrades_to_lexical_without_vector_backend() -> None:
    store = MemoryStore()
    store.remember("local agent", source="doc")
    result = await HybridRetriever(RetrievalEngine(store)).retrieve(MemoryQuery("local", top_k=1))
    assert result.strategy == "lexical"
    assert result.hits
