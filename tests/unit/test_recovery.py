import pytest

from aios.recovery import RecoveryDecision, RetryRecoveryHandler


def test_retry_handler_retries_until_limit_then_aborts() -> None:
    handler = RetryRecoveryHandler(max_retries=2)
    error = RuntimeError("transient")

    assert handler.decide(error, attempt=1) is RecoveryDecision.RETRY
    assert handler.decide(error, attempt=2) is RecoveryDecision.RETRY
    assert handler.decide(error, attempt=3) is RecoveryDecision.ABORT


def test_retry_handler_with_zero_retries_aborts_immediately() -> None:
    handler = RetryRecoveryHandler(max_retries=0)

    assert handler.decide(RuntimeError("terminal"), attempt=1) is RecoveryDecision.ABORT


def test_retry_handler_rejects_negative_retry_configuration() -> None:
    with pytest.raises(ValueError):
        RetryRecoveryHandler(max_retries=-1)
