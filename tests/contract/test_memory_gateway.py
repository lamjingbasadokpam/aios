from uuid import uuid4

import pytest

from aios.memory import MemoryAccessContext, MemoryGateway, MemoryQuery, MemoryScope, MemoryStore


def test_gateway_allows_authorized_agent_scope() -> None:
    gateway = MemoryGateway(MemoryStore())
    context = MemoryAccessContext(agent_id=uuid4())

    record = gateway.remember(
        "agent memory",
        source="test",
        context=context,
        scope=MemoryScope.AGENT,
    )

    assert record.scope is MemoryScope.AGENT


def test_gateway_denies_unauthorized_scope() -> None:
    gateway = MemoryGateway(MemoryStore())
    context = MemoryAccessContext(agent_id=uuid4())

    with pytest.raises(PermissionError):
        gateway.remember(
            "user memory",
            source="test",
            context=context,
            scope=MemoryScope.USER,
        )


def test_gateway_allows_explicitly_granted_scope() -> None:
    gateway = MemoryGateway(MemoryStore())
    context = MemoryAccessContext(
        agent_id=uuid4(),
        user_id=uuid4(),
        allowed_scopes=frozenset({MemoryScope.AGENT, MemoryScope.USER}),
    )

    record = gateway.remember(
        "user memory",
        source="test",
        context=context,
        scope=MemoryScope.USER,
    )

    assert record.scope is MemoryScope.USER


def test_gateway_recall_cannot_cross_scope() -> None:
    store = MemoryStore()
    gateway = MemoryGateway(store)
    context = MemoryAccessContext(agent_id=uuid4())

    store.remember(
        "private user fact",
        source="test",
        namespace="user-1",
        scope=MemoryScope.USER,
    )

    with pytest.raises(PermissionError):
        gateway.recall(
            MemoryQuery(query="private fact", namespace="user-1", scope=MemoryScope.USER),
            context=context,
        )


def test_gateway_recall_defaults_to_agent_scope() -> None:
    store = MemoryStore()
    gateway = MemoryGateway(store)
    context = MemoryAccessContext(agent_id=uuid4())

    gateway.remember(
        "agent fact",
        source="test",
        namespace="agent-1",
        context=context,
        scope=MemoryScope.AGENT,
    )

    hits = gateway.recall(
        MemoryQuery(query="agent fact", namespace="agent-1"),
        context=context,
    )

    assert len(hits) == 1


def test_gateway_update_and_forget_enforce_scope() -> None:
    store = MemoryStore()
    gateway = MemoryGateway(store)
    owner = MemoryAccessContext(agent_id=uuid4())
    other = MemoryAccessContext(agent_id=uuid4())

    record = gateway.remember("owned fact", source="test", context=owner)

    with pytest.raises(PermissionError):
        gateway.update_content(record.memory_id, "tampered", context=other)

    with pytest.raises(PermissionError):
        gateway.forget(record.memory_id, context=other)

    updated = gateway.update_content(record.memory_id, "updated", context=owner)
    assert updated.content == "updated"
    assert gateway.forget(record.memory_id, context=owner) is True


def test_gateway_rejects_invalid_namespace() -> None:
    gateway = MemoryGateway(MemoryStore())
    context = MemoryAccessContext(agent_id=uuid4())

    with pytest.raises(ValueError):
        gateway.remember("fact", source="test", namespace=" bad", context=context)


def test_gateway_does_not_expose_raw_memory_dependencies() -> None:
    gateway = MemoryGateway(MemoryStore())

    assert not hasattr(gateway, "store")
    assert not hasattr(gateway, "retriever")
