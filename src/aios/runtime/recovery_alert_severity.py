"""Normalized severity for recovery alerts."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum

from .recovery_alerts import RecoveryAlert


class RecoveryAlertSeverity(IntEnum):
    INFO = 1
    WARNING = 2
    CRITICAL = 3


@dataclass(frozen=True, slots=True)
class ClassifiedRecoveryAlert:
    alert: RecoveryAlert
    severity: RecoveryAlertSeverity


class RecoveryAlertSeverityClassifier:
    """Maps recovery alert codes to operational severity."""

    def __init__(self, mapping: dict[str, RecoveryAlertSeverity] | None = None) -> None:
        self._mapping = mapping or {
            "slow_recovery": RecoveryAlertSeverity.WARNING,
            "recovery_failures": RecoveryAlertSeverity.CRITICAL,
            "recovery_aborts": RecoveryAlertSeverity.CRITICAL,
        }

    def classify(self, alert: RecoveryAlert) -> ClassifiedRecoveryAlert:
        severity = self._mapping.get(alert.code, RecoveryAlertSeverity.INFO)
        return ClassifiedRecoveryAlert(alert, severity)
