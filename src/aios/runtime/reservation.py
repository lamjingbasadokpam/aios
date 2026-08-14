"""Resource reservation primitives for concurrent AIOS admission."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from .budget import ResourceBudget, ResourceUsage


@dataclass(frozen=True, slots=True)
class ResourceReservation:
    reservation_id: str
    usage: ResourceUsage


class ReservationManager:
    """In-memory reservation ledger with fail-closed capacity checks."""

    def __init__(self, budget: ResourceBudget) -> None:
        self.budget = budget
        self._reserved = ResourceUsage()
        self._reservations: dict[str, ResourceUsage] = {}

    def reserve(self, usage: ResourceUsage) -> ResourceReservation | None:
        projected = ResourceUsage(
            tokens=self._reserved.tokens + usage.tokens,
            runtime_seconds=self._reserved.runtime_seconds + usage.runtime_seconds,
            tool_calls=self._reserved.tool_calls + usage.tool_calls,
            retries=self._reserved.retries + usage.retries,
            cost=self._reserved.cost + usage.cost,
        )
        if not self._within_budget(projected):
            return None
        reservation = ResourceReservation(str(uuid4()), usage)
        self._reservations[reservation.reservation_id] = usage
        self._reserved = projected
        return reservation

    def release(self, reservation_id: str) -> bool:
        usage = self._reservations.pop(reservation_id, None)
        if usage is None:
            return False
        self._reserved = ResourceUsage(
            tokens=self._reserved.tokens - usage.tokens,
            runtime_seconds=max(0.0, self._reserved.runtime_seconds - usage.runtime_seconds),
            tool_calls=self._reserved.tool_calls - usage.tool_calls,
            retries=self._reserved.retries - usage.retries,
            cost=max(0.0, self._reserved.cost - usage.cost),
        )
        return True

    def _within_budget(self, usage: ResourceUsage) -> bool:
        checks = (
            (self.budget.max_tokens, usage.tokens),
            (self.budget.max_runtime_seconds, usage.runtime_seconds),
            (self.budget.max_tool_calls, usage.tool_calls),
            (self.budget.max_retries, usage.retries),
            (self.budget.max_cost, usage.cost),
        )
        return all(limit is None or value <= limit for limit, value in checks)

    @property
    def reserved(self) -> ResourceUsage:
        return self._reserved
