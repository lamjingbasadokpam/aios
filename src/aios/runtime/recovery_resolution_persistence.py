"""Durable, replayable recovery resolution records."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable


@dataclass(frozen=True, slots=True)
class RecoveryResolutionRecord:
    effect_key: str
    resolution: str
    sequence: int

    def payload(self) -> dict[str, Any]:
        return {
            "effect_key": self.effect_key,
            "resolution": self.resolution,
            "sequence": self.sequence,
        }


class RecoveryResolutionStore:
    """Append-only adapter for durable recovery resolution events."""

    EVENT_TYPE = "recovery_resolution"

    def __init__(self, append_event: Callable[[str, dict[str, Any]], None]) -> None:
        self._append_event = append_event

    def persist(self, record: RecoveryResolutionRecord) -> None:
        self._append_event(self.EVENT_TYPE, record.payload())

    @staticmethod
    def replay(records: Iterable[RecoveryResolutionRecord]) -> dict[str, RecoveryResolutionRecord]:
        latest: dict[str, RecoveryResolutionRecord] = {}
        for record in records:
            current = latest.get(record.effect_key)
            if current is None or record.sequence >= current.sequence:
                latest[record.effect_key] = record
        return latest
