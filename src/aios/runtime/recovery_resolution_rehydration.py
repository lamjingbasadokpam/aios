"""Rehydrate recovery, incident, and alert state from durable resolutions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .recovery_alert_events import RecoveryAlertEvent
from .recovery_alert_lifecycle import RecoveryAlertLifecycleTracker
from .recovery_incident import RecoveryIncident
from .recovery_incident_lifecycle import RecoveryIncidentLifecycleTracker, RecoveryIncidentState
from .recovery_resolution_persistence import RecoveryResolutionRecord, RecoveryResolutionStore


@dataclass(frozen=True, slots=True)
class RecoveryRehydratedState:
    resolution: RecoveryResolutionRecord | None
    incident_state: RecoveryIncidentState | None
    alerts_resolved: bool


class RecoveryResolutionRehydrator:
    """Reconstructs operational recovery state deterministically during startup."""

    def rehydrate(
        self,
        effect_key: str,
        resolutions: Iterable[RecoveryResolutionRecord],
        incident: RecoveryIncident,
        events: Iterable[RecoveryAlertEvent],
    ) -> RecoveryRehydratedState:
        latest = RecoveryResolutionStore.replay(resolutions).get(effect_key)
        history = tuple(events)
        incident_status = RecoveryIncidentLifecycleTracker().update(incident, history)
        alert_states = RecoveryAlertLifecycleTracker().update(history)
        alerts_resolved = bool(alert_states) and all(not state.active for state in alert_states.values())
        if latest is not None and latest.resolution == "resolved":
            return RecoveryRehydratedState(latest, RecoveryIncidentState.RESOLVED, True)
        return RecoveryRehydratedState(latest, incident_status.state, alerts_resolved)
