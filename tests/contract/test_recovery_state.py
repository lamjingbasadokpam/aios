from aios.runtime.effect_recovery_events import EffectRecoveryEvent, EffectRecoveryEventType
from aios.runtime.recovery_state import RecoveryStateRehydrator


def test_rehydration_rebuilds_committed_effect() -> None:
    events = [
        EffectRecoveryEvent(
            EffectRecoveryEventType.EFFECT_REUSED,
            "effect-1",
            "already committed",
            "ok",
        )
    ]
    state = RecoveryStateRehydrator().rehydrate(events)
    assert state.effects["effect-1"].state == "committed"
    assert state.effects["effect-1"].result == "ok"
    assert RecoveryStateRehydrator().is_safe_to_resume(state)


def test_rehydration_blocks_resume_when_reconciliation_is_required() -> None:
    events = [
        EffectRecoveryEvent(
            EffectRecoveryEventType.EFFECT_RECONCILIATION_REQUIRED,
            "effect-2",
            "lease expired",
        )
    ]
    rehydrator = RecoveryStateRehydrator()
    state = rehydrator.rehydrate(events)
    assert not rehydrator.is_safe_to_resume(state)
