"""Heartbeat renewal for long-running AIOS effect leases."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .effect_lease import EffectLease, EffectLeaseStore


@dataclass(frozen=True, slots=True)
class LeaseHeartbeat:
    key: str
    owner: str
    ttl_seconds: int = 60

    def renew(self, store: EffectLeaseStore) -> EffectLease:
        return store.renew(self.key, self.owner, self.ttl_seconds)


class LeaseHeartbeatRunner:
    """Small synchronous heartbeat primitive; scheduling remains caller-owned."""

    def __init__(self, heartbeat: LeaseHeartbeat, store: EffectLeaseStore) -> None:
        self.heartbeat = heartbeat
        self.store = store

    def tick(self) -> EffectLease:
        return self.heartbeat.renew(self.store)

    def run_ticks(self, count: int, on_tick: Callable[[EffectLease], None] | None = None) -> EffectLease:
        if count < 1:
            raise ValueError("count must be positive")
        lease = self.tick()
        if on_tick:
            on_tick(lease)
        for _ in range(count - 1):
            lease = self.tick()
            if on_tick:
                on_tick(lease)
        return lease
