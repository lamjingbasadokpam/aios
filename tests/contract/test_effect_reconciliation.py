from aios.runtime.effect_lease import EffectLeaseStore, LeaseStatus
from aios.runtime.effect_reconciliation import EffectRecoveryAction, EffectReconciler


def test_committed_effect_reuses_result() -> None:
    store = EffectLeaseStore()
    store.claim("effect-1", "worker-a")
    store.commit("effect-1", "worker-a", "ok")
    decision = EffectReconciler(store).decide("effect-1", "worker-a")
    assert decision.action == EffectRecoveryAction.REUSE_RESULT
    assert decision.result == "ok"


def test_unknown_effect_requires_reconciliation() -> None:
    decision = EffectReconciler(EffectLeaseStore()).decide("missing", "worker-a")
    assert decision.action == EffectRecoveryAction.RECONCILE


def test_other_owner_aborts() -> None:
    store = EffectLeaseStore()
    store.claim("effect-1", "worker-a")
    decision = EffectReconciler(store).decide("effect-1", "worker-b")
    assert decision.action == EffectRecoveryAction.ABORT


def test_explicit_failure_can_retry() -> None:
    store = EffectLeaseStore()
    store.claim("effect-1", "worker-a")
    store.fail("effect-1", "worker-a", "provider rejected")
    decision = EffectReconciler(store).decide("effect-1", "worker-a")
    assert decision.action == EffectRecoveryAction.RETRY
