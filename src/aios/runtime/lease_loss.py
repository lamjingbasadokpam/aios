"""Lease-loss detection for AIOS effect execution."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from .effect_lease import EffectLeaseStore, LeaseStatus


class LeaseLossAction(str, Enum):
    ABORT_COMMIT = "abort_commit"
    RECONCILE = "reconcile"
    RESUME_OWNERSHIP = "resume_ownership"


@dataclass(frozen=True, slots=True)
class LeaseLossResult:
    action: LeaseLossAction
    reason: str
    result: Any = None


class LeaseLossDetector:
    """Determines what an executor may safely do after losing lease ownership."""

    def __init__(self, store: EffectLeaseStore) -> None:
        self.store = store

    def inspect(self, key: str, owner: str) -> LeaseLossResult:
        lease = self.store._leases.get(key)
        if lease is None:
            return LeaseLossResult(LeaseLossAction.RECONCILE, "lease record is missing")
        if lease.status == LeaseStatus.COMMITTED:
            return LeaseLossResult(LeaseLossAction.RECONCILE, "effect already committed", lease.result)
        if lease.owner != owner:
            return LeaseLossResult(LeaseLossAction.ABORT_COMMIT, "lease ownership belongs to another worker")
        if lease.expired():
            return LeaseLossResult(LeaseLossAction.RECONCILE, "lease expired before completion")
        return LeaseLossResult(LeaseLossAction.RESUME_OWNERSHIP, "lease is still owned and active")
