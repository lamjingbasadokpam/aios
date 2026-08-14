import pytest

from aios.memory.contracts import MemoryRecord
from aios.memory.vector import HashEmbedder, InMemoryVectorIndex


@pytest.mark.asyncio
async def test_hash_embedder_is_local_and_deterministic_for_a_process() -> None:
    embedder = HashEmbedder(32)
    vectors = await embedder.embed(["hello world", "hello world"])
    assert vectors[0] == vectors[1]
    assert len(vectors[0]) == 32


@pytest.mark.asyncio
async def test_vector_index_returns_namespace_scoped_hits() -> None:
    embedder = HashEmbedder(32)
    records = [
        MemoryRecord("AIOS local agent", "test", "a"),
        MemoryRecord("unrelated", "test", "b"),
    ]
    vectors = await embedder.embed([r.content for r in records])
    index = InMemoryVectorIndex()
    await index.upsert(records, vectors)
    query = (await embedder.embed(["AIOS local agent"]))[0]
    hits = await index.search(query, namespace="default", top_k=2)
    assert hits
    assert hits[0].record.content == "AIOS local agent"
