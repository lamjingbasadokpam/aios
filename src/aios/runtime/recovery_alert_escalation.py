"""Time-based escalation for persistent recovery alerts."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .recovery_alert_events import RecoveryAlertEvent
from .recovery_alert_severity import RecoveryAlertSeverity


@dataclass(frozen=True, slots=True)
class RecoveryEscalationPolicy:
    escalation_after_seconds: float
    from_severity: RecoveryAlertSeverity = RecoveryAlertSeverity.WARNING
    to_severity: RecoveryAlertSeverity = RecoveryAlertSeverity.CRITICAL


@dataclass(frozen=True, slots=True)
class RecoveryEscalation:
    event: RecoveryAlertEvent
    severity: RecoveryAlertSeverity
    escalated: bool
    elapsed_seconds: float


class RecoveryAlertEscalator:
    """Escalates a persistent alert once its configured age is exceeded."""

    def __init__(self, policy: RecoveryEscalationPolicy) -> None:
        self.policy = policy

    def evaluate(
        self,
        event: RecoveryAlertEvent,
        started_at: datetime,
        now: datetime,
        severity: RecoveryAlertSeverity,
    ) -> RecoveryEscalation:
        elapsed = max(0.0, (now - started_at).total_seconds())
        escalated = (
            severity >= self.policy.from_severity
            and elapsed > self.policy.escalation_after_seconds
            and severity < self.policy.to_severity
        )
        return RecoveryEscalation(
            event=event,
            severity=self.policy.to_severity if escalated else severity,
            escalated=escalated,
            elapsed_seconds=elapsed,
        )
