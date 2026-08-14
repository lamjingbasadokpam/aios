from datetime import datetime, timedelta, timezone

import pytest

from aios.runtime.effect_lease import EffectLeaseStore, LeaseStatus


def test_second_owner_cannot_take_live_lease() -> None:
    store = EffectLeaseStore()
    first = store.claim("effect-1", "worker-a")
    second = store.claim("effect-1", "worker-b")
    assert first.owner == "worker-a"
    assert second.owner == "worker-a"
    assert second.status == LeaseStatus.IN_FLIGHT


def test_owner_can_renew_and_commit() -> None:
    store = EffectLeaseStore()
    store.claim("effect-1", "worker-a")
    renewed = store.renew("effect-1", "worker-a")
    committed = store.commit("effect-1", "worker-a", "ok")
    assert renewed.owner == "worker-a"
    assert committed.status == LeaseStatus.COMMITTED
    assert committed.result == "ok"


def test_expired_lease_can_be_reclaimed() -> None:
    store = EffectLeaseStore()
    store.claim("effect-1", "worker-a")
    store._leases["effect-1"] = store._leases["effect-1"].__class__(
        "effect-1", "worker-a", datetime.now(timezone.utc) - timedelta(seconds=1)
    )
    store.expire("effect-1")
    replacement = store.claim("effect-1", "worker-b")
    assert replacement.owner == "worker-b"
    assert replacement.status == LeaseStatus.IN_FLIGHT


def test_non_owner_cannot_renew() -> None:
    store = EffectLeaseStore()
    store.claim("effect-1", "worker-a")
    with pytest.raises(RuntimeError):
        store.renew("effect-1", "worker-b")
