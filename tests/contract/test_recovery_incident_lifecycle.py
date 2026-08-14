from datetime import datetime, timezone

from aios.runtime.recovery_alert_events import RecoveryAlertEvent
from aios.runtime.recovery_incident import RecoveryIncidentCorrelator
from aios.runtime.recovery_incident_lifecycle import RecoveryIncidentLifecycleTracker, RecoveryIncidentState


def test_incident_starts_open() -> None:
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    incident = RecoveryIncidentCorrelator().correlate("e1", [], start)
    status = RecoveryIncidentLifecycleTracker().update(incident, [])
    assert status.state == RecoveryIncidentState.OPEN


def test_incident_can_escalate_then_resolve() -> None:
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    incident = RecoveryIncidentCorrelator().correlate("e1", [], start)
    tracker = RecoveryIncidentLifecycleTracker()
    escalated = RecoveryAlertEvent("incident_escalated", "incident escalated", 1, 1)
    resolved = RecoveryAlertEvent("incident_resolved", "incident resolved", 1, 1)
    status = tracker.update(incident, [escalated])
    assert status.state == RecoveryIncidentState.ESCALATED
    status = tracker.update(incident, [escalated, resolved])
    assert status.state == RecoveryIncidentState.RESOLVED
