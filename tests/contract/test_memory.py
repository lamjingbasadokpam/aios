from datetime import datetime, timedelta, timezone

import pytest

from aios.memory import (
    MemoryQuery,
    MemoryRecord,
    MemoryRetriever,
    MemoryScope,
    MemoryStore,
    MemoryType,
    RagPipeline,
)


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


def test_memory_contract_supports_typed_scoped_records() -> None:
    store = MemoryStore()
    record = store.remember(
        "user prefers concise answers",
        source="agent",
        namespace="user-1",
        memory_type=MemoryType.SEMANTIC,
        scope=MemoryScope.USER,
        metadata={"preference": "style"},
    )

    assert record.memory_type is MemoryType.SEMANTIC
    assert record.scope is MemoryScope.USER
    assert store.query_candidates(
        MemoryQuery(
            query="preferences",
            namespace="user-1",
            memory_type=MemoryType.SEMANTIC,
            scope=MemoryScope.USER,
        )
    ) == [record]


def test_memory_update_preserves_identity() -> None:
    store = MemoryStore()
    record = store.remember("old fact", source="agent")

    updated = store.update_content(record.memory_id, "new fact")

    assert updated.memory_id == record.memory_id
    assert updated.content == "new fact"
    assert store.list() == [updated]


def test_memory_revision_can_supersede_previous_record() -> None:
    store = MemoryStore()
    original = store.remember("prefers dark mode", source="agent")
    revision = store.remember(
        "prefers light mode",
        source="agent",
        supersedes_id=original.memory_id,
    )

    assert revision.supersedes_id == original.memory_id
    assert {r.memory_id for r in store.list()} == {original.memory_id, revision.memory_id}


def test_expired_memory_is_not_retrievable() -> None:
    store = MemoryStore()
    expired = store.remember(
        "temporary context",
        source="session",
        expires_at=datetime.now(timezone.utc) - timedelta(seconds=1),
    )

    assert expired.is_expired()
    assert store.list() == []
    assert store.query_candidates(MemoryQuery(query="temporary")) == []


def test_memory_forget_is_idempotent() -> None:
    store = MemoryStore()
    record = store.remember("forget me", source="agent")

    assert store.forget(record.memory_id) is True
    assert store.forget(record.memory_id) is False
    assert store.list() == []


def test_update_unknown_memory_fails_explicitly() -> None:
    store = MemoryStore()
    with pytest.raises(KeyError):
        store.update_content(__import__("uuid").uuid4(), "updated")
