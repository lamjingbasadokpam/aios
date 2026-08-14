"""Idempotency-aware execution boundary for AIOS effects."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .effect_identity import EffectIntent
from .idempotency import EffectRegistry, EffectStatus


@dataclass(frozen=True, slots=True)
class EffectExecution:
    key: str
    executed: bool
    result: Any = None


class EffectExecutionBoundary:
    """Ensures a committed logical effect is not executed again in registry scope."""

    def __init__(self, registry: EffectRegistry) -> None:
        self.registry = registry

    def execute(self, intent: EffectIntent, operation: Callable[[], Any]) -> EffectExecution:
        key = intent.key()
        record = self.registry.begin(key)
        if record.status == EffectStatus.COMMITTED:
            return EffectExecution(key, False, record.result)
        if record.status == EffectStatus.FAILED:
            raise RuntimeError(f"effect {key} previously failed")
        result = operation()
        self.registry.commit(key, result)
        return EffectExecution(key, True, result)
