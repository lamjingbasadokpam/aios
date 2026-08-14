from aios.runtime.effect_lease import EffectLeaseStore
from aios.runtime.lease_heartbeat import LeaseHeartbeat, LeaseHeartbeatRunner


def test_heartbeat_renews_owned_lease() -> None:
    store = EffectLeaseStore()
    lease = store.claim("effect-1", "worker-a", ttl_seconds=10)
    runner = LeaseHeartbeatRunner(LeaseHeartbeat("effect-1", "worker-a", 30), store)
    renewed = runner.tick()
    assert renewed.owner == "worker-a"
    assert renewed.expires_at > lease.expires_at


def test_heartbeat_rejects_wrong_owner() -> None:
    store = EffectLeaseStore()
    store.claim("effect-1", "worker-a")
    runner = LeaseHeartbeatRunner(LeaseHeartbeat("effect-1", "worker-b"), store)
    try:
        runner.tick()
    except RuntimeError as exc:
        assert "not owned" in str(exc)
    else:
        raise AssertionError("expected ownership failure")
