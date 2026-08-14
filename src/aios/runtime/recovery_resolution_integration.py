"""Integrate recovery resolution with incident and alert lifecycle state."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .recovery_alert_events import RecoveryAlertEvent
from .recovery_alert_lifecycle import RecoveryAlertLifecycleTracker
from .recovery_incident import RecoveryIncident
from .recovery_incident_lifecycle import RecoveryIncidentLifecycleTracker, RecoveryIncidentStatus, RecoveryIncidentState


@dataclass(frozen=True, slots=True)
class RecoveryResolutionResult:
    incident: RecoveryIncident
    incident_status: RecoveryIncidentStatus
    alerts_resolved: bool


class RecoveryResolutionIntegrator:
    """Derives operational resolution from the persisted recovery event history."""

    def __init__(self) -> None:
        self._incident_tracker = RecoveryIncidentLifecycleTracker()
        self._alert_tracker = RecoveryAlertLifecycleTracker()

    def resolve(self, incident: RecoveryIncident, events: Iterable[RecoveryAlertEvent]) -> RecoveryResolutionResult:
        history = tuple(events)
        incident_status = self._incident_tracker.update(incident, history)
        alert_states = self._alert_tracker.update(history)
        alerts_resolved = all(not state.active for state in alert_states.values())
        if incident_status.state != RecoveryIncidentState.RESOLVED:
            alerts_resolved = False
        return RecoveryResolutionResult(incident, incident_status, alerts_resolved)
