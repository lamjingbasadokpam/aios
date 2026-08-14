from aios.runtime.effect_recovery_events import EffectRecoveryEvent, EffectRecoveryEventType
from aios.runtime.recovery_completion import RecoveryCompletionCoordinator
from aios.runtime.recovery_runtime import RecoveryMode, RecoveryRuntimeController


def test_restart_during_recovery_remains_blocked_until_resolution() -> None:
    required = EffectRecoveryEvent(EffectRecoveryEventType.EFFECT_RECONCILIATION_REQUIRED, "e1", "crash")
    controller = RecoveryRuntimeController()
    first = controller.startup([required])
    second = controller.startup([required])
    assert first.mode == second.mode == RecoveryMode.RECOVERY_REQUIRED


def test_duplicate_resolution_is_idempotent_for_rehydration() -> None:
    coordinator = RecoveryCompletionCoordinator()
    required = EffectRecoveryEvent(EffectRecoveryEventType.EFFECT_RECONCILIATION_REQUIRED, "e1", "lease lost")
    resolved = coordinator.resolution_event("e1", "confirmed")
    events = [required, resolved, resolved]
    assert coordinator.complete(events).completed is True


def test_unknown_effect_never_becomes_retryable_from_recovery_history() -> None:
    controller = RecoveryRuntimeController()
    unknown = EffectRecoveryEvent(EffectRecoveryEventType.EFFECT_RECONCILIATION_REQUIRED, "e2", "outcome unknown")
    status = controller.startup([unknown])
    assert status.mode == RecoveryMode.RECOVERY_REQUIRED


def test_resolution_after_restart_restores_normal_mode() -> None:
    controller = RecoveryRuntimeController()
    required = EffectRecoveryEvent(EffectRecoveryEventType.EFFECT_RECONCILIATION_REQUIRED, "e3", "worker crashed")
    resolved = RecoveryCompletionCoordinator().resolution_event("e3", "confirmed")
    assert controller.startup([required]).mode == RecoveryMode.RECOVERY_REQUIRED
    assert controller.startup([required, resolved]).mode == RecoveryMode.NORMAL
