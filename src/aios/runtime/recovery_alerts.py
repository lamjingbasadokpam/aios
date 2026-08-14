"""Threshold-based alerts for unhealthy effect recovery behavior."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .recovery_observability import RecoveryObservation


@dataclass(frozen=True, slots=True)
class RecoveryAlertThresholds:
    max_recovery_duration_seconds: float | None = None
    max_failed_observations: int | None = None
    max_aborted_observations: int | None = None


@dataclass(frozen=True, slots=True)
class RecoveryAlert:
    code: str
    message: str
    value: float | int
    threshold: float | int


class RecoveryAlertEvaluator:
    def __init__(self, thresholds: RecoveryAlertThresholds) -> None:
        self.thresholds = thresholds

    def evaluate(self, observations: Iterable[RecoveryObservation]) -> list[RecoveryAlert]:
        items = list(observations)
        alerts: list[RecoveryAlert] = []
        durations = [x.recovery_duration_seconds for x in items if x.recovery_duration_seconds is not None]
        if self.thresholds.max_recovery_duration_seconds is not None and durations:
            maximum = max(durations)
            if maximum > self.thresholds.max_recovery_duration_seconds:
                alerts.append(RecoveryAlert("slow_recovery", "recovery duration exceeded threshold", maximum, self.thresholds.max_recovery_duration_seconds))
        failed = sum(x.state == "failed" for x in items)
        if self.thresholds.max_failed_observations is not None and failed > self.thresholds.max_failed_observations:
            alerts.append(RecoveryAlert("recovery_failures", "recovery failure count exceeded threshold", failed, self.thresholds.max_failed_observations))
        aborted = sum(x.state == "aborted" for x in items)
        if self.thresholds.max_aborted_observations is not None and aborted > self.thresholds.max_aborted_observations:
            alerts.append(RecoveryAlert("recovery_aborts", "recovery abort count exceeded threshold", aborted, self.thresholds.max_aborted_observations))
        return alerts
