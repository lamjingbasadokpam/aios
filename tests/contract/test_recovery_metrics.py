from datetime import datetime, timedelta, timezone

from aios.runtime.recovery_metrics import RecoveryMetricsCollector
from aios.runtime.recovery_observability import RecoveryObservation


def test_metrics_aggregate_states_and_durations() -> None:
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    observations = [
        RecoveryObservation("e1", "reconciled", "ok", started_at=start, resolved_at=start + timedelta(seconds=10)),
        RecoveryObservation("e2", "reconciled", "ok", started_at=start, resolved_at=start + timedelta(seconds=20)),
        RecoveryObservation("e3", "aborted", "failed"),
    ]
    metrics = RecoveryMetricsCollector().collect(observations)
    assert metrics.total == 3
    assert metrics.by_state == {"reconciled": 2, "aborted": 1}
    assert metrics.average_duration_seconds == 15
    assert metrics.p95_duration_seconds == 19.5
