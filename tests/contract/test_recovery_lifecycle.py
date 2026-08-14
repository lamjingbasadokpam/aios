from aios.runtime.effect_recovery_events import EffectRecoveryEvent, EffectRecoveryEventType
from aios.runtime.recovery_completion import RecoveryCompletionCoordinator
from aios.runtime.recovery_runtime import RecoveryMode, RecoveryRuntimeController


def test_end_to_end_recovery_lifecycle() -> None:
    controller = RecoveryRuntimeController()
    required = EffectRecoveryEvent(
        EffectRecoveryEventType.EFFECT_RECONCILIATION_REQUIRED,
        "effect-1",
        "worker lease expired",
    )

    status = controller.startup([required])
    assert status.mode == RecoveryMode.RECOVERY_REQUIRED

    completion = RecoveryCompletionCoordinator()
    resolved = completion.resolution_event("effect-1", "confirmed")
    status = controller.startup([required, resolved])

    assert status.mode == RecoveryMode.NORMAL
    assert completion.complete([required, resolved]).completed is True
