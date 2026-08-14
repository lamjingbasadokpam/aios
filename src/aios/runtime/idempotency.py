"""Idempotency and effect deduplication primitives for AIOS runtime actions."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from threading import Lock
from typing import Any


class EffectStatus(str, Enum):
    NEW = "new"
    IN_FLIGHT = "in_flight"
    COMMITTED = "committed"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class EffectRecord:
    key: str
    status: EffectStatus
    result: Any = None


class EffectRegistry:
    """Process-local registry preventing duplicate committed effects."""

    def __init__(self) -> None:
        self._records: dict[str, EffectRecord] = {}
        self._lock = Lock()

    def begin(self, key: str) -> EffectRecord:
        with self._lock:
            existing = self._records.get(key)
            if existing is not None:
                return existing
            record = EffectRecord(key, EffectStatus.IN_FLIGHT)
            self._records[key] = record
            return record

    def commit(self, key: str, result: Any = None) -> EffectRecord:
        with self._lock:
            if key not in self._records:
                raise KeyError(key)
            record = EffectRecord(key, EffectStatus.COMMITTED, result)
            self._records[key] = record
            return record

    def fail(self, key: str, result: Any = None) -> EffectRecord:
        with self._lock:
            if key not in self._records:
                raise KeyError(key)
            record = EffectRecord(key, EffectStatus.FAILED, result)
            self._records[key] = record
            return record

    def get(self, key: str) -> EffectRecord | None:
        with self._lock:
            return self._records.get(key)
