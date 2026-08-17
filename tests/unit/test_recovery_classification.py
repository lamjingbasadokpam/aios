from aios.recovery.classification import RecoveryClass, classify_failure


def test_timeout_is_transient():
    assert classify_failure(TimeoutError("timeout")) is RecoveryClass.TRANSIENT


def test_connection_failure_is_transient():
    assert classify_failure(ConnectionError("offline")) is RecoveryClass.TRANSIENT


def test_permission_failure_is_policy():
    assert classify_failure(PermissionError("denied")) is RecoveryClass.POLICY


def test_invalid_input_is_terminal():
    assert classify_failure(ValueError("bad input")) is RecoveryClass.TERMINAL


def test_unknown_failure_is_transient_for_v0():
    assert classify_failure(RuntimeError("provider failed")) is RecoveryClass.TRANSIENT
