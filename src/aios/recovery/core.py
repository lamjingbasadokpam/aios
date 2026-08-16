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

    def __post_init__(self) -> None:
        if self.max_retries < 0:
            raise ValueError("max_retries must be non-negative")

    def decide(self, error: Exception, attempt: int) -> RecoveryDecision:
        del error
        if attempt < 1:
            raise ValueError("attempt must be positive")
        return RecoveryDecision.RETRY if attempt <= self.max_retries else RecoveryDecision.ABORT
