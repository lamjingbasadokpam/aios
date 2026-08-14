import pytest

from aios.memory.contracts import MemoryQuery, MemoryRecord
from aios.memory.retrieval import RetrievalEngine
from aios.memory.store import MemoryStore


@pytest.mark.asyncio
async def test_retrieval_uses_lexical_fallback() -> None:
    store = MemoryStore()
    store.remember("AIOS uses provider-neutral adapters", source="test")
    store.remember("unrelated note", source="test")
    result = await RetrievalEngine(store).retrieve(MemoryQuery("provider-neutral", top_k=1))
    assert result.strategy == "lexical"
    assert len(result.hits) == 1
    assert "provider-neutral" in result.hits[0].record.content


class Embedder:
    async def embed(self, texts):
        return [[1.0, 0.0] for _ in texts]


class Index:
    async def upsert(self, records, vectors):
        self.records = records
        self.vectors = vectors

    async def search(self, vector, *, namespace, top_k):
        return []


@pytest.mark.asyncio
async def test_vector_path_is_provider_neutral() -> None:
    engine = RetrievalEngine(MemoryStore(), Embedder(), Index())
    result = await engine.retrieve(MemoryQuery("hello", top_k=3))
    assert result.strategy == "vector"
    assert result.hits == ()
