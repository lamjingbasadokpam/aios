from aios.runtime.budget import ResourceBudget, ResourceUsage
from aios.runtime.reservation import ReservationManager


def test_reservation_prevents_overcommit() -> None:
    manager = ReservationManager(ResourceBudget(max_tool_calls=2))
    first = manager.reserve(ResourceUsage(tool_calls=2))
    second = manager.reserve(ResourceUsage(tool_calls=1))
    assert first is not None
    assert second is None
    assert manager.reserved.tool_calls == 2


def test_release_returns_capacity() -> None:
    manager = ReservationManager(ResourceBudget(max_tokens=100))
    reservation = manager.reserve(ResourceUsage(tokens=80))
    assert reservation is not None
    assert manager.release(reservation.reservation_id) is True
    assert manager.reserved.tokens == 0
    assert manager.reserve(ResourceUsage(tokens=100)) is not None
