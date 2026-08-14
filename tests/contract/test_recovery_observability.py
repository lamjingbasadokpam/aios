from datetime import datetime, timezone

from aios.runtime.recovery_observability import RecoveryObservation, RecoveryObserver


def test_observation_preserves_recovery_context() -> None:
    seen = []
    observer = RecoveryObserver(seen.append)
    started = datetime(2026, 1, 1, tzinfo=timezone.utc)
    resolved = datetime(2026, 1, 1, 0, 0, 12, tzinfo=timezone.utc)
    observation = RecoveryObservation(
        effect_key="effect-1",
        state="reconciled",
        reason="lease expired",
        owner="worker-a",
        attempt=2,
        started_at=started,
        resolved_at=resolved,
        result="confirmed",
    )
    observer.observe(observation)
    assert seen == [observation]
    assert observation.recovery_duration_seconds == 12.0
