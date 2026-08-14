from aios.runtime.effect_recovery_events import EffectRecoveryEvent, EffectRecoveryEventType
from aios.runtime.recovery_completion import RecoveryCompletionCoordinator


def test_recovery_cannot_complete_with_unresolved_effect() -> None:
    events = [EffectRecoveryEvent(
        EffectRecoveryEventType.EFFECT_RECONCILIATION_REQUIRED,
        "effect-1",
        "lease expired",
    )]
    result = RecoveryCompletionCoordinator().complete(events)
    assert result.completed is False


def test_recovery_completes_after_resolution() -> None:
    coordinator = RecoveryCompletionCoordinator()
    events = [
        EffectRecoveryEvent(
            EffectRecoveryEventType.EFFECT_RECONCILIATION_REQUIRED,
            "effect-1",
            "lease expired",
        ),
        coordinator.resolution_event("effect-1", "confirmed"),
    ]
    result = coordinator.complete(events)
    assert result.completed is True
