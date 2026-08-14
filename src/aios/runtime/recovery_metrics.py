"""Aggregate operational metrics for effect recovery."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Iterable

from .recovery_observability import RecoveryObservation


@dataclass(frozen=True, slots=True)
class RecoveryMetrics:
    total: int
    by_state: dict[str, int]
    average_duration_seconds: float | None
    p95_duration_seconds: float | None


class RecoveryMetricsCollector:
    """Builds deterministic aggregate metrics from structured observations."""

    def collect(self, observations: Iterable[RecoveryObservation]) -> RecoveryMetrics:
        items = list(observations)
        counts: dict[str, int] = {}
        durations = []
        for item in items:
            counts[item.state] = counts.get(item.state, 0) + 1
            duration = item.recovery_duration_seconds
            if duration is not None:
                durations.append(duration)
        return RecoveryMetrics(
            total=len(items),
            by_state=counts,
            average_duration_seconds=mean(durations) if durations else None,
            p95_duration_seconds=self._percentile95(durations) if durations else None,
        )

    @staticmethod
    def _percentile95(values: list[float]) -> float:
        ordered = sorted(values)
        if len(ordered) == 1:
            return ordered[0]
        rank = 0.95 * (len(ordered) - 1)
        lower = int(rank)
        upper = min(lower + 1, len(ordered) - 1)
        fraction = rank - lower
        return ordered[lower] + (ordered[upper] - ordered[lower]) * fraction
