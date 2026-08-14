from datetime import datetime, timezone

from aios.runtime.effect_lease import EffectLease, EffectLeaseStore, LeaseStatus
from aios.runtime.lease_loss import LeaseLossAction, LeaseLossDetector


def test_other_worker_causes_commit_abort() -> None:
    store = EffectLeaseStore()
    store.claim("effect-1", "worker-a")
    result = LeaseLossDetector(store).inspect("effect-1", "worker-b")
    assert result.action == LeaseLossAction.ABORT_COMMIT


def test_committed_effect_requires_reconciliation() -> None:
    store = EffectLeaseStore()
    store.claim("effect-1", "worker-a")
    store.commit("effect-1", "worker-a", "ok")
    result = LeaseLossDetector(store).inspect("effect-1", "worker-a")
    assert result.action == LeaseLossAction.RECONCILE
    assert result.result == "ok"


def test_active_owner_can_continue() -> None:
    store = EffectLeaseStore()
    store.claim("effect-1", "worker-a")
    result = LeaseLossDetector(store).inspect("effect-1", "worker-a")
    assert result.action == LeaseLossAction.RESUME_OWNERSHIP
