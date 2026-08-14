from datetime import datetime, timezone

from aios.runtime.recovery_alert_events import RecoveryAlertEvent
from aios.runtime.recovery_incident import RecoveryIncidentCorrelator


def test_related_alerts_share_one_recovery_incident() -> None:
    started = datetime(2026, 1, 1, tzinfo=timezone.utc)
    alerts = [
        RecoveryAlertEvent("slow_recovery", "too slow", 42, 30),
        RecoveryAlertEvent("recovery_failures", "failed", 3, 1),
    ]
    incident = RecoveryIncidentCorrelator().correlate("effect-1", alerts, started)
    assert incident.incident_id == "recovery:effect-1"
    assert incident.effect_key == "effect-1"
    assert incident.alerts == tuple(alerts)
    assert incident.started_at == started
