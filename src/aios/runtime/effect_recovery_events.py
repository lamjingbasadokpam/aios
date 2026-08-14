"""Durable event records for effect recovery decisions."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable


class EffectRecoveryEventType(str, Enum):
    EFFECT_RECONCILIATION_REQUIRED = "effect_reconciliation_required"
    EFFECT_REUSED = "effect_reused"
    EFFECT_RETRIED = "effect_retried"
    EFFECT_RECOVERY_ABORTED = "effect_recovery_aborted"


@dataclass(frozen=True, slots=True)
class EffectRecoveryEvent:
    event_type: EffectRecoveryEventType
    effect_key: str
    reason: str
    result: Any = None


class EffectRecoveryEventSink:
    """Small event sink contract; durable event stores can implement this interface."""

    def __init__(self, append: Callable[[EffectRecoveryEvent], None]) -> None:
        self._append = append

    def emit(self, event: EffectRecoveryEvent) -> None:
        self._append(event)
