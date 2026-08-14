"""Coordinates effect reconciliation after lease loss or runtime recovery."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .effect_reconciliation import EffectRecoveryAction, EffectReconciler


@dataclass(frozen=True, slots=True)
class EffectRecoveryResult:
    action: EffectRecoveryAction
    result: Any = None
    reason: str = ""


class EffectRecoveryCoordinator:
    """Single recovery entry point; retries only effects known to have failed."""

    def __init__(self, reconciler: EffectReconciler) -> None:
        self.reconciler = reconciler

    def recover(
        self,
        key: str,
        owner: str,
        retry: Callable[[], Any] | None = None,
    ) -> EffectRecoveryResult:
        decision = self.reconciler.decide(key, owner)
        if decision.action == EffectRecoveryAction.REUSE_RESULT:
            return EffectRecoveryResult(decision.action, decision.result, decision.reason)
        if decision.action != EffectRecoveryAction.RETRY:
            return EffectRecoveryResult(decision.action, decision.result, decision.reason)
        if retry is None:
            return EffectRecoveryResult(EffectRecoveryAction.ABORT, reason="retry requested but no retry operation was supplied")
        result = retry()
        return EffectRecoveryResult(EffectRecoveryAction.RETRY, result, "explicitly failed effect retried")
