from aios.memory import MemoryQuery, MemoryRecord, MemoryRetriever, MemoryStore, RagPipeline


def test_memory_retrieval_and_namespace_filtering() -> None:
    store = MemoryStore()
    store.add(MemoryRecord(content="AIOS uses a model router", source="architecture", namespace="aios"))
    store.add(MemoryRecord(content="unrelated note", source="other", namespace="other"))

    retriever = MemoryRetriever(store)
    hits = retriever.search(MemoryQuery(query="model router", namespace="aios", top_k=3))

    assert len(hits) == 1
    assert hits[0].record.source == "architecture"
    assert hits[0].score > 0


def test_rag_pipeline_assembles_context() -> None:
    store = MemoryStore()
    store.add(MemoryRecord(content="Tool execution passes through policy", source="docs"))
    context = RagPipeline(MemoryRetriever(store)).augment("How does tool execution work?")
    assert "Relevant memory:" in context
    assert "Tool execution passes through policy" in context
