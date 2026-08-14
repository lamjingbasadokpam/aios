"""Reservation settlement and reconciliation for AIOS runtime budgets."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .budget import ResourceUsage
from .reservation import ReservationManager


class SettlementStatus(str, Enum):
    SETTLED = "settled"
    OVERAGE = "overage"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class SettlementResult:
    status: SettlementStatus
    reserved: ResourceUsage
    actual: ResourceUsage
    released: ResourceUsage
    overage: ResourceUsage


class SettlementManager:
    """Settles a reservation against explicit actual usage and releases its capacity."""

    def __init__(self, reservations: ReservationManager) -> None:
        self.reservations = reservations

    def settle(self, reservation_id: str, actual: ResourceUsage) -> SettlementResult:
        reserved = self.reservations._reservations.get(reservation_id)
        if reserved is None:
            return SettlementResult(
                SettlementStatus.UNKNOWN,
                ResourceUsage(), actual, ResourceUsage(), actual,
            )

        released = ResourceUsage(
            tokens=max(0, reserved.tokens - actual.tokens),
            runtime_seconds=max(0.0, reserved.runtime_seconds - actual.runtime_seconds),
            tool_calls=max(0, reserved.tool_calls - actual.tool_calls),
            retries=max(0, reserved.retries - actual.retries),
            cost=max(0.0, reserved.cost - actual.cost),
        )
        overage = ResourceUsage(
            tokens=max(0, actual.tokens - reserved.tokens),
            runtime_seconds=max(0.0, actual.runtime_seconds - reserved.runtime_seconds),
            tool_calls=max(0, actual.tool_calls - reserved.tool_calls),
            retries=max(0, actual.retries - reserved.retries),
            cost=max(0.0, actual.cost - reserved.cost),
        )
        self.reservations.release(reservation_id)
        status = SettlementStatus.OVERAGE if any((overage.tokens, overage.runtime_seconds, overage.tool_calls, overage.retries, overage.cost)) else SettlementStatus.SETTLED
        return SettlementResult(status, reserved, actual, released, overage)
