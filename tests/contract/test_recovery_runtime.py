import pytest

from aios.runtime.effect_recovery_events import EffectRecoveryEvent, EffectRecoveryEventType
from aios.runtime.recovery_runtime import RecoveryMode, RecoveryRuntimeController


def test_startup_enters_normal_mode_when_recovery_is_clean() -> None:
    controller = RecoveryRuntimeController()
    status = controller.startup([
        EffectRecoveryEvent(EffectRecoveryEventType.EFFECT_REUSED, "effect-1", "committed", "ok")
    ])
    assert status.mode == RecoveryMode.NORMAL
    controller.require_execution(status)


def test_startup_blocks_execution_when_reconciliation_is_required() -> None:
    controller = RecoveryRuntimeController()
    status = controller.startup([
        EffectRecoveryEvent(EffectRecoveryEventType.EFFECT_RECONCILIATION_REQUIRED, "effect-1", "lease expired")
    ])
    assert status.mode == RecoveryMode.RECOVERY_REQUIRED
    with pytest.raises(RuntimeError, match="recovery is required"):
        controller.require_execution(status)
