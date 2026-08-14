import pytest

from aios.runtime.budget import ResourceBudget, ResourceUsage
from aios.runtime.cancellation import CancellationReason
from aios.runtime.control import InMemoryRuntimeController
from aios.runtime.lifecycle import LifecycleState, RuntimeLifecycle
from aios.runtime.reservation import ReservationManager


def make_lifecycle() -> RuntimeLifecycle:
    return RuntimeLifecycle(
        InMemoryRuntimeController(),
        ReservationManager(ResourceBudget(max_tokens=1000)),
    )


def test_lifecycle_create_admit_reserve_and_settle() -> None:
    lifecycle = make_lifecycle()
    run = lifecycle.create("run-1")
    assert run.state == LifecycleState.CREATED
    lifecycle.admit(run)
    lifecycle.reserve(run, ResourceUsage(tokens=500))
    assert run.state == LifecycleState.RUNNING
    result = lifecycle.settle(run, ResourceUsage(tokens=300))
    assert result.released.tokens == 200
    assert run.state == LifecycleState.COMPLETED


def test_lifecycle_cancellation_survives_settlement() -> None:
    lifecycle = make_lifecycle()
    run = lifecycle.create("run-2")
    lifecycle.admit(run)
    lifecycle.reserve(run, ResourceUsage(tokens=100))
    lifecycle.cancel(run, CancellationReason.USER)
    assert run.state == LifecycleState.CANCELLED
    lifecycle.settle(run, ResourceUsage(tokens=10))
    assert run.state == LifecycleState.CANCELLED
    assert run.cancellation.cancelled


def test_lifecycle_requires_admission_before_reservation() -> None:
    lifecycle = make_lifecycle()
    run = lifecycle.create("run-3")
    with pytest.raises(ValueError, match="admitted"):
        lifecycle.reserve(run, ResourceUsage(tokens=1))
