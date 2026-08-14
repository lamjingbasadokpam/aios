from datetime import datetime, timezone

from aios.runtime.recovery_alert_events import RecoveryAlertEvent
from aios.runtime.recovery_incident import RecoveryIncident
from aios.runtime.recovery_resolution_integration import RecoveryResolutionIntegrator


def test_recovery_resolution_closes_incident_and_alerts() -> None:
    incident = RecoveryIncident("recovery:e1", "e1", (), datetime(2026, 1, 1, tzinfo=timezone.utc))
    alert = RecoveryAlertEvent("slow_recovery", "too slow", 42, 30)
    resolved_alert = RecoveryAlertEvent("resolved:slow_recovery", "resolved", 42, 30)
    resolved_incident = RecoveryAlertEvent("incident_resolved", "recovery confirmed", 1, 1)

    result = RecoveryResolutionIntegrator().resolve(
        incident,
        [alert, resolved_alert, resolved_incident],
    )

    assert result.incident_status.state.value == "resolved"
    assert result.alerts_resolved is True
