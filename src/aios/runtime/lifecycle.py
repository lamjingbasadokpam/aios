"""Unified runtime lifecycle orchestration for AIOS runs."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .budget import ResourceUsage
from .cancellation import CancellationReason, CancellationRequest, CancellationToken
from .control import InMemoryRuntimeController, RunHandle, RunState
from .reservation import ReservationManager, ResourceReservation
from .settlement import SettlementManager, SettlementResult


class LifecycleState(str, Enum):
    CREATED = "created"
    ADMITTED = "admitted"
    RESERVED = "reserved"
    RUNNING = "running"
    SETTLING = "settling"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"


@dataclass(slots=True)
class RuntimeRun:
    run: RunHandle
    state: LifecycleState = LifecycleState.CREATED
    cancellation: CancellationToken = None  # type: ignore[assignment]
    reservation: ResourceReservation | None = None

    def __post_init__(self) -> None:
        if self.cancellation is None:
            self.cancellation = CancellationToken()


class RuntimeLifecycle:
    """Small orchestration boundary connecting control, reservation and settlement."""

    def __init__(self, controller: InMemoryRuntimeController, reservations: ReservationManager) -> None:
        self.controller = controller
        self.reservations = reservations
        self.settlements = SettlementManager(reservations)

    def create(self, run_id: str) -> RuntimeRun:
        return RuntimeRun(self.controller.register(run_id))

    def admit(self, runtime_run: RuntimeRun) -> None:
        if runtime_run.state != LifecycleState.CREATED:
            raise ValueError("run is not in created state")
        runtime_run.state = LifecycleState.ADMITTED

    def reserve(self, runtime_run: RuntimeRun, estimate: ResourceUsage) -> ResourceReservation:
        if runtime_run.state != LifecycleState.ADMITTED:
            raise ValueError("run must be admitted before reservation")
        reservation = self.reservations.reserve(estimate)
        if reservation is None:
            raise RuntimeError("resource reservation denied")
        runtime_run.reservation = reservation
        runtime_run.state = LifecycleState.RESERVED
        runtime_run.run.state = RunState.RUNNING
        runtime_run.state = LifecycleState.RUNNING
        return reservation

    def cancel(self, runtime_run: RuntimeRun, reason: CancellationReason, message: str = "") -> None:
        runtime_run.cancellation.cancel(CancellationRequest(runtime_run.run.run_id, reason, message))
        runtime_run.run.state = RunState.CANCELLED
        runtime_run.state = LifecycleState.CANCELLED

    def settle(self, runtime_run: RuntimeRun, actual: ResourceUsage) -> SettlementResult:
        if runtime_run.reservation is None:
            raise ValueError("run has no reservation")
        if runtime_run.state not in {LifecycleState.RUNNING, LifecycleState.CANCELLED}:
            raise ValueError("run is not executable or cancellable")
        runtime_run.state = LifecycleState.SETTLING
        result = self.settlements.settle(runtime_run.reservation.reservation_id, actual)
        runtime_run.reservation = None
        if runtime_run.state == LifecycleState.SETTLING:
            runtime_run.state = LifecycleState.CANCELLED if runtime_run.cancellation.cancelled else LifecycleState.COMPLETED
        runtime_run.run.state = RunState.CANCELLED if runtime_run.cancellation.cancelled else RunState.COMPLETED
        return result
