from aios.runtime.durable_effects import DurableEffectStatus, InMemoryDurableEffectStore


def test_atomic_claim_reference_store_returns_existing_claim() -> None:
    store = InMemoryDurableEffectStore()
    first = store.claim("effect-1")
    second = store.claim("effect-1")
    assert first is not None
    assert first.status == DurableEffectStatus.IN_FLIGHT
    assert second == first


def test_commit_is_visible_to_subsequent_claim() -> None:
    store = InMemoryDurableEffectStore()
    store.claim("effect-1")
    committed = store.commit("effect-1", "ok")
    assert committed.status == DurableEffectStatus.COMMITTED
    assert store.claim("effect-1") == committed
