"""Lifecycle state tracking for correlated recovery incidents."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Iterable

from .recovery_alert_events import RecoveryAlertEvent
from .recovery_incident import RecoveryIncident


class RecoveryIncidentState(StrEnum):
    OPEN = "open"
    ESCALATED = "escalated"
    RESOLVED = "resolved"


@dataclass(frozen=True, slots=True)
class RecoveryIncidentStatus:
    incident: RecoveryIncident
    state: RecoveryIncidentState
    alerts: tuple[RecoveryAlertEvent, ...]


class RecoveryIncidentLifecycleTracker:
    """Derives incident state from its ordered alert history."""

    def update(self, incident: RecoveryIncident, events: Iterable[RecoveryAlertEvent]) -> RecoveryIncidentStatus:
        alerts = tuple(events)
        state = RecoveryIncidentState.OPEN
        for event in alerts:
            if event.code == "incident_resolved":
                state = RecoveryIncidentState.RESOLVED
            elif event.code == "incident_escalated" and state != RecoveryIncidentState.RESOLVED:
                state = RecoveryIncidentState.ESCALATED
        return RecoveryIncidentStatus(incident, state, alerts)
