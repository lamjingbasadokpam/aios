from dataclasses import replace
from uuid import uuid4

import pytest

from aios.memory import MemoryAccessContext, MemoryGateway, MemoryStore, MemoryAccessDenied


def test_gateway_update_cannot_forge_owner_or_scope() -> None:
    store = MemoryStore()
    gateway = MemoryGateway(store)
    owner = MemoryAccessContext(agent_id=uuid4())
    attacker = MemoryAccessContext(agent_id=uuid4())

    record = gateway.remember("owned fact", source="test", context=owner)
    forged = replace(record, owner_id=attacker.agent_id)

    with pytest.raises(MemoryAccessDenied):
        gateway.update(forged, context=attacker)


def test_gateway_update_preserves_stored_identity_and_ownership() -> None:
    store = MemoryStore()
    gateway = MemoryGateway(store)
    owner = MemoryAccessContext(agent_id=uuid4())

    record = gateway.remember("owned fact", source="test", context=owner)
    updated = replace(record, content="updated fact")

    result = gateway.update(updated, context=owner)

    assert result.memory_id == record.memory_id
    assert result.owner_id == record.owner_id
    assert result.scope == record.scope
    assert result.content == "updated fact"
