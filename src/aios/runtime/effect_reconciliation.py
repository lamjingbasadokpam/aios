"""Translate lease/effect observations into conservative recovery actions."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from .effect_lease import EffectLeaseStore, LeaseStatus


class EffectRecoveryAction(str, Enum):
    REUSE_RESULT = "reuse_result"
    RECONCILE = "reconcile"
    RETRY = "retry"
    ABORT = "abort"


@dataclass(frozen=True, slots=True)
class EffectRecoveryDecision:
    action: EffectRecoveryAction
    reason: str
    result: Any = None


class EffectReconciler:
    """Conservative effect recovery: unknown external state never retries blindly."""

    def __init__(self, store: EffectLeaseStore) -> None:
        self.store = store

    def decide(self, key: str, owner: str) -> EffectRecoveryDecision:
        lease = self.store._leases.get(key)
        if lease is None:
            return EffectRecoveryDecision(EffectRecoveryAction.RECONCILE, "effect state is unknown")
        if lease.status == LeaseStatus.COMMITTED:
            return EffectRecoveryDecision(EffectRecoveryAction.REUSE_RESULT, "effect is already committed", lease.result)
        if lease.owner != owner:
            return EffectRecoveryDecision(EffectRecoveryAction.ABORT, "effect is owned by another worker")
        if lease.status == LeaseStatus.EXPIRED or lease.expired():
            return EffectRecoveryDecision(EffectRecoveryAction.RECONCILE, "lease expired; external outcome is unknown")
        if lease.status == LeaseStatus.FAILED:
            return EffectRecoveryDecision(EffectRecoveryAction.RETRY, "effect is explicitly known to have failed")
        return EffectRecoveryDecision(EffectRecoveryAction.RECONCILE, "effect remains in-flight")
