from aios.runtime.budget import ResourceBudget, ResourceUsage
from aios.runtime.reservation import ReservationManager
from aios.runtime.settlement import SettlementManager, SettlementStatus


def test_settlement_releases_unused_capacity() -> None:
    reservations = ReservationManager(ResourceBudget(max_tokens=1000))
    reservation = reservations.reserve(ResourceUsage(tokens=1000))
    assert reservation is not None
    result = SettlementManager(reservations).settle(reservation.reservation_id, ResourceUsage(tokens=600))
    assert result.status == SettlementStatus.SETTLED
    assert result.released.tokens == 400
    assert reservations.reserved.tokens == 0


def test_settlement_reports_overage() -> None:
    reservations = ReservationManager(ResourceBudget(max_tokens=1000))
    reservation = reservations.reserve(ResourceUsage(tokens=500))
    assert reservation is not None
    result = SettlementManager(reservations).settle(reservation.reservation_id, ResourceUsage(tokens=700))
    assert result.status == SettlementStatus.OVERAGE
    assert result.overage.tokens == 200
