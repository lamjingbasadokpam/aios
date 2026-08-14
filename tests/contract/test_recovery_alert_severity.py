from aios.runtime.recovery_alerts import RecoveryAlert
from aios.runtime.recovery_alert_severity import RecoveryAlertSeverity, RecoveryAlertSeverityClassifier


def test_known_alerts_get_expected_severity() -> None:
    classifier = RecoveryAlertSeverityClassifier()
    assert classifier.classify(RecoveryAlert("slow_recovery", "slow", 40, 30)).severity == RecoveryAlertSeverity.WARNING
    assert classifier.classify(RecoveryAlert("recovery_failures", "failed", 5, 2)).severity == RecoveryAlertSeverity.CRITICAL
    assert classifier.classify(RecoveryAlert("recovery_aborts", "aborted", 3, 1)).severity == RecoveryAlertSeverity.CRITICAL


def test_unknown_alert_defaults_to_info() -> None:
    result = RecoveryAlertSeverityClassifier().classify(RecoveryAlert("new_condition", "new", 1, 0))
    assert result.severity == RecoveryAlertSeverity.INFO
