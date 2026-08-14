from aios.runtime.effect_lease import EffectLeaseStore, LeaseStatus
from aios.runtime.effect_reconciliation import EffectRecoveryAction, EffectReconciler
from aios.runtime.effect_recovery import EffectRecoveryCoordinator


def test_coordinator_reuses_committed_result() -> None:
    store = EffectLeaseStore()
    store.claim("effect-1", "worker-a")
    store.commit("effect-1", "worker-a", "ok")
    result = EffectRecoveryCoordinator(EffectReconciler(store)).recover("effect-1", "worker-a")
    assert result.action == EffectRecoveryAction.REUSE_RESULT
    assert result.result == "ok"


def test_coordinator_does_not_blindly_retry_unknown_effect() -> None:
    store = EffectLeaseStore()
    result = EffectRecoveryCoordinator(EffectReconciler(store)).recover("missing", "worker-a", lambda: "bad")
    assert result.action == EffectRecoveryAction.RECONCILE


def test_coordinator_retries_explicit_failure() -> None:
    store = EffectLeaseStore()
    store.claim("effect-1", "worker-a")
    store._leases["effect-1"] = store._leases["effect-1"].__class__(
        "effect-1", "worker-a", store._leases["effect-1"].expires_at, LeaseStatus.FAILED
    )
    result = EffectRecoveryCoordinator(EffectReconciler(store)).recover("effect-1", "worker-a", lambda: "retried")
    assert result.action == EffectRecoveryAction.RETRY
    assert result.result == "retried"
