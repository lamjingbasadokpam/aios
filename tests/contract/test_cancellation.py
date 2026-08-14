import pytest

from aios.runtime.cancellation import CancellationReason, CancellationRequest, CancellationToken


def test_cancellation_is_idempotent_and_preserves_first_reason() -> None:
    token = CancellationToken()
    token.cancel(CancellationRequest("run-1", CancellationReason.OVERAGE, "budget exceeded"))
    token.cancel(CancellationRequest("run-1", CancellationReason.USER, "stop"))
    assert token.cancelled
    assert token.request is not None
    assert token.request.reason == CancellationReason.OVERAGE


def test_raise_if_cancelled() -> None:
    token = CancellationToken()
    token.cancel(CancellationRequest("run-1", CancellationReason.USER))
    with pytest.raises(RuntimeError, match="cancelled: user"):
        token.raise_if_cancelled()
