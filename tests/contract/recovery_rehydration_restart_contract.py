from datetime import datetime, timezone

from aios.runtime.recovery_alert_events import RecoveryAlertEvent
from aios.runtime.recovery_incident import RecoveryIncident
from aios.runtime.recovery_incident_lifecycle import RecoveryIncidentState
from aios.runtime.recovery_resolution_persistence import RecoveryResolutionRecord
from aios.runtime.recovery_resolution_rehydration import RecoveryResolutionRehydrator


def test_rehydration_preserves_resolved_state() -> None:
    started = datetime(2026, 1, 1, tzinfo=timezone.utc)
    incident = RecoveryIncident("recovery:e1", "e1", (), started)
    resolution = RecoveryResolutionRecord("e1", "resolved", 4)
    events = [
        RecoveryAlertEvent("slow_recovery", "too slow", 42, 30),
        RecoveryAlertEvent("resolved:slow_recovery", "resolved", 42, 30),
        RecoveryAlertEvent("incident_resolved", "recovery confirmed", 1, 1),
    ]
    state = RecoveryResolutionRehydrator().rehydrate("e1", [resolution], incident, events)
    assert state.resolution == resolution
    assert state.incident_state == RecoveryIncidentState.RESOLVED
    assert state.alerts_resolved is True
