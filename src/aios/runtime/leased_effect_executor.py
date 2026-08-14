"""Lease-aware effect execution boundary for AIOS."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .effect_identity import EffectIntent
from .effect_lease import EffectLeaseStore, LeaseStatus


@dataclass(frozen=True, slots=True)
class LeasedEffectExecution:
    key: str
    executed: bool
    result: Any = None


class LeasedEffectExecutor:
    """Executes an effect only while its worker owns an active lease."""

    def __init__(self, leases: EffectLeaseStore) -> None:
        self.leases = leases

    def execute(
        self,
        intent: EffectIntent,
        owner: str,
        operation: Callable[[], Any],
        ttl_seconds: int = 60,
    ) -> LeasedEffectExecution:
        key = intent.key()
        lease = self.leases.claim(key, owner, ttl_seconds)
        if lease.status == LeaseStatus.COMMITTED:
            return LeasedEffectExecution(key, False, lease.result)
        if lease.owner != owner or lease.status != LeaseStatus.IN_FLIGHT:
            raise RuntimeError("effect lease is owned by another worker")

        try:
            result = operation()
            self.leases.commit(key, owner, result)
            return LeasedEffectExecution(key, True, result)
        except Exception as exc:
            # The lease remains in-flight so a recovery worker can reconcile
            # the external effect rather than assuming the side effect failed.
            raise exc
