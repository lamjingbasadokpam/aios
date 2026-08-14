"""Adapter that persists effect recovery events through the runtime event store."""

from __future__ import annotations

from typing import Any, Callable

from .effect_recovery_events import EffectRecoveryEvent, EffectRecoveryEventSink


class RuntimeRecoveryEventStore:
    """Maps recovery events into the existing durable runtime-event append API."""

    def __init__(self, append_event: Callable[[str, dict[str, Any]], None]) -> None:
        self._append_event = append_event
        self.sink = EffectRecoveryEventSink(self._persist)

    def emit(self, event: EffectRecoveryEvent) -> None:
        self.sink.emit(event)

    def _persist(self, event: EffectRecoveryEvent) -> None:
        payload = {
            "effect_key": event.effect_key,
            "reason": event.reason,
            "result": event.result,
        }
        self._append_event(event.event_type.value, payload)
