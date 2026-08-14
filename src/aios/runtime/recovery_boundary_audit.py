"""Boundary checks for the recovery observability and resolution pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .recovery_alert_events import RecoveryAlertEvent
from .recovery_incident import RecoveryIncident
from .recovery_resolution_persistence import RecoveryResolutionRecord
from .recovery_resolution_rehydration import RecoveryResolutionRehydrator


@dataclass(frozen=True, slots=True)
class RecoveryBoundaryAudit:
    effect_key: str
    has_resolution: bool
    resolution_replayable: bool
    incident_rehydrated: bool
    alerts_rehydrated: bool

    @property
    def clean(self) -> bool:
        return (
            self.has_resolution
            and self.resolution_replayable
            and self.incident_rehydrated
            and self.alerts_rehydrated
        )


class RecoveryBoundaryAuditor:
    """Verifies that durable resolution reconstructs the same operational boundary."""

    def audit(
        self,
        effect_key: str,
        resolutions: Iterable[RecoveryResolutionRecord],
        incident: RecoveryIncident,
        events: Iterable[RecoveryAlertEvent],
    ) -> RecoveryBoundaryAudit:
        records = tuple(resolutions)
        latest = max((r for r in records if r.effect_key == effect_key), key=lambda r: r.sequence, default=None)
        state = RecoveryResolutionRehydrator().rehydrate(effect_key, records, incident, events)
        resolved = latest is not None and latest.resolution == "resolved"
        return RecoveryBoundaryAudit(
            effect_key=effect_key,
            has_resolution=latest is not None,
            resolution_replayable=state.resolution == latest if latest is not None else False,
            incident_rehydrated=state.incident_state.value == "resolved" if resolved and state.incident_state else False,
            alerts_rehydrated=state.alerts_resolved if resolved else False,
        )
