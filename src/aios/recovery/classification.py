"""Failure classification for the AIOS V0 recovery boundary."""

from __future__ import annotations

from enum import StrEnum


class RecoveryClass(StrEnum):
    TRANSIENT = "transient"
    TERMINAL = "terminal"
    POLICY = "policy"


def classify_failure(error: Exception) -> RecoveryClass:
    """Classify a runtime failure without coupling recovery to tool implementations."""
    if isinstance(error, (TimeoutError, ConnectionError, OSError)):
        return RecoveryClass.TRANSIENT
    if isinstance(error, PermissionError):
        return RecoveryClass.POLICY
    if isinstance(error, (ValueError, TypeError, KeyError, AttributeError, NotImplementedError)):
        return RecoveryClass.TERMINAL
    return RecoveryClass.TRANSIENT
