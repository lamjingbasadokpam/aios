"""Provider-neutral cooperative cancellation protocol for AIOS runs."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CancellationReason(str, Enum):
    USER = "user"
    OVERAGE = "overage"
    SHUTDOWN = "shutdown"
    POLICY = "policy"
    TIMEOUT = "timeout"


@dataclass(frozen=True, slots=True)
class CancellationRequest:
    run_id: str
    reason: CancellationReason
    message: str = ""


class CancellationToken:
    """Cooperative cancellation token checked by execution boundaries."""

    def __init__(self) -> None:
        self._request: CancellationRequest | None = None

    @property
    def cancelled(self) -> bool:
        return self._request is not None

    @property
    def request(self) -> CancellationRequest | None:
        return self._request

    def cancel(self, request: CancellationRequest) -> None:
        if self._request is None:
            self._request = request

    def raise_if_cancelled(self) -> None:
        if self._request is not None:
            raise RuntimeError(
                f"run {self._request.run_id} cancelled: {self._request.reason.value}"
            )
