"""Lease ownership and stale-claim recovery for durable effects."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from threading import Lock
from typing import Any


class LeaseStatus(str, Enum):
    IN_FLIGHT = "in_flight"
    COMMITTED = "committed"
    FAILED = "failed"
    EXPIRED = "expired"


@dataclass(frozen=True, slots=True)
class EffectLease:
    key: str
    owner: str
    expires_at: datetime
    status: LeaseStatus = LeaseStatus.IN_FLIGHT
    result: Any = None

    def expired(self, now: datetime | None = None) -> bool:
        now = now or datetime.now(timezone.utc)
        return now >= self.expires_at


class EffectLeaseStore:
    """Reference lease store; production implementations must make claim/renew atomic."""

    def __init__(self) -> None:
        self._leases: dict[str, EffectLease] = {}
        self._lock = Lock()

    def claim(self, key: str, owner: str, ttl_seconds: int = 60) -> EffectLease:
        with self._lock:
            current = self._leases.get(key)
            if current is not None and current.status == LeaseStatus.COMMITTED:
                return current
            if current is not None and not current.expired() and current.owner != owner:
                return current
            lease = EffectLease(key, owner, datetime.now(timezone.utc) + timedelta(seconds=ttl_seconds))
            self._leases[key] = lease
            return lease

    def renew(self, key: str, owner: str, ttl_seconds: int = 60) -> EffectLease:
        with self._lock:
            current = self._leases.get(key)
            if current is None or current.owner != owner or current.status != LeaseStatus.IN_FLIGHT:
                raise RuntimeError("lease is not owned by caller")
            lease = EffectLease(key, owner, datetime.now(timezone.utc) + timedelta(seconds=ttl_seconds))
            self._leases[key] = lease
            return lease

    def commit(self, key: str, owner: str, result: Any = None) -> EffectLease:
        with self._lock:
            current = self._leases.get(key)
            if current is None or current.owner != owner:
                raise RuntimeError("lease is not owned by caller")
            lease = EffectLease(key, owner, current.expires_at, LeaseStatus.COMMITTED, result)
            self._leases[key] = lease
            return lease

    def fail(self, key: str, owner: str, result: Any = None) -> EffectLease:
        with self._lock:
            current = self._leases.get(key)
            if current is None or current.owner != owner:
                raise RuntimeError("lease is not owned by caller")
            lease = EffectLease(key, owner, current.expires_at, LeaseStatus.FAILED, result)
            self._leases[key] = lease
            return lease

    def expire(self, key: str) -> EffectLease | None:
        with self._lock:
            current = self._leases.get(key)
            if current is None or current.status != LeaseStatus.IN_FLIGHT or not current.expired():
                return current
            lease = EffectLease(key, current.owner, current.expires_at, LeaseStatus.EXPIRED, current.result)
            self._leases[key] = lease
            return lease
