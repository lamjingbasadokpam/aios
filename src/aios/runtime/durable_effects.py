"""Durable effect registry contract for cross-process idempotency."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Protocol


class DurableEffectStatus(str, Enum):
    IN_FLIGHT = "in_flight"
    COMMITTED = "committed"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class DurableEffectRecord:
    key: str
    status: DurableEffectStatus
    result: Any = None


class DurableEffectStore(Protocol):
    """Atomic shared-store contract required by distributed workers."""

    def claim(self, key: str) -> DurableEffectRecord | None: ...

    def commit(self, key: str, result: Any = None) -> DurableEffectRecord: ...

    def fail(self, key: str, result: Any = None) -> DurableEffectRecord: ...

    def get(self, key: str) -> DurableEffectRecord | None: ...


class InMemoryDurableEffectStore:
    """Reference implementation; production stores must provide atomic claim."""

    def __init__(self) -> None:
        self._records: dict[str, DurableEffectRecord] = {}

    def claim(self, key: str) -> DurableEffectRecord | None:
        existing = self._records.get(key)
        if existing is not None:
            return existing
        record = DurableEffectRecord(key, DurableEffectStatus.IN_FLIGHT)
        self._records[key] = record
        return record

    def commit(self, key: str, result: Any = None) -> DurableEffectRecord:
        if key not in self._records:
            raise KeyError(key)
        record = DurableEffectRecord(key, DurableEffectStatus.COMMITTED, result)
        self._records[key] = record
        return record

    def fail(self, key: str, result: Any = None) -> DurableEffectRecord:
        if key not in self._records:
            raise KeyError(key)
        record = DurableEffectRecord(key, DurableEffectStatus.FAILED, result)
        self._records[key] = record
        return record

    def get(self, key: str) -> DurableEffectRecord | None:
        return self._records.get(key)
