from datetime import datetime, timedelta, timezone

from aios.runtime.recovery_alert_escalation import RecoveryEscalationPolicy, RecoveryAlertEscalator
from aios.runtime.recovery_alert_events import RecoveryAlertEvent
from aios.runtime.recovery_alert_severity import RecoveryAlertSeverity


def test_persistent_warning_escalates_to_critical() -> None:
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    event = RecoveryAlertEvent("slow_recovery", "too slow", 42, 30)
    result = RecoveryAlertEscalator(
        RecoveryEscalationPolicy(30)
    ).evaluate(event, start, start + timedelta(seconds=31), RecoveryAlertSeverity.WARNING)
    assert result.escalated is True
    assert result.severity == RecoveryAlertSeverity.CRITICAL


def test_warning_before_threshold_does_not_escalate() -> None:
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    event = RecoveryAlertEvent("slow_recovery", "too slow", 20, 30)
    result = RecoveryAlertEscalator(RecoveryEscalationPolicy(30)).evaluate(
        event, start, start + timedelta(seconds=30), RecoveryAlertSeverity.WARNING
    )
    assert result.escalated is False
    assert result.severity == RecoveryAlertSeverity.WARNING
