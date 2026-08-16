"""Small, deterministic recovery contract for AIOS V0."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol


class RecoveryDecision(StrEnum):
    RETRY = "retry"
    ABORT = "abort"


class RecoveryHandler(Protocol):
    def decide(self, error: Exception, attempt: int) -> RecoveryDecision: ...


@dataclass(frozen=True, slots=True)
class RetryRecoveryHandler:
    max_retries: int = 2

    def decide(self, error: Exception, attempt: int) -> RecoveryDecision:
        del error
        return RecoveryDecision.RETRY if attempt <= self.max_retries else RecoveryDecision.ABORT
