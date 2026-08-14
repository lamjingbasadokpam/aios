"""Idempotency-aware execution boundary for AIOS effects."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .idempotency import EffectRegistry, EffectStatus


@dataclass(frozen=True, slots=True)
class EffectExecution:
    key: str
    executed: bool
    result: Any = None


class EffectExecutionBoundary:
    """Ensures a committed effect is not executed again within the registry scope."""

    def __init__(self, registry: EffectRegistry) -> None:
        self.registry = registry

    def execute(self, key: str, operation: Callable[[], Any]) -> EffectExecution:
        record = self.registry.begin(key)
        if record.status == EffectStatus.COMMITTED:
            return EffectExecution(key, False, record.result)
        if record.status == EffectStatus.IN_FLIGHT:
            # The current process owns this reservation; callers must reconcile
            # an in-flight effect rather than silently duplicate it.
            existing = self.registry.get(key)
            if existing is not None and existing.status == EffectStatus.IN_FLIGHT:
                result = operation()
                self.registry.commit(key, result)
                return EffectExecution(key, True, result)
        try:
            result = operation()
            self.registry.commit(key, result)
            return EffectExecution(key, True, result)
        except Exception as exc:
            self.registry.fail(key, exc)
            raise
