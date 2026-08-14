"""Correlate related recovery alerts into operational incidents."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

from .recovery_alert_events import RecoveryAlertEvent


@dataclass(frozen=True, slots=True)
class RecoveryIncident:
    incident_id: str
    effect_key: str
    alerts: tuple[RecoveryAlertEvent, ...]
    started_at: datetime


class RecoveryIncidentCorrelator:
    """Groups recovery alerts sharing an effect identity into one incident."""

    def correlate(
        self,
        effect_key: str,
        events: Iterable[RecoveryAlertEvent],
        started_at: datetime,
    ) -> RecoveryIncident:
        alerts = tuple(events)
        incident_id = f"recovery:{effect_key}"
        return RecoveryIncident(incident_id, effect_key, alerts, started_at)
