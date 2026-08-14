from aios.runtime.effect_recovery_events import EffectRecoveryEvent, EffectRecoveryEventType
from aios.runtime.recovery_replay import RecoveryEventReplayer


def test_replay_reconstructs_committed_result() -> None:
    events = [
        EffectRecoveryEvent(
            EffectRecoveryEventType.EFFECT_RECONCILIATION_REQUIRED,
            "effect-1",
            "lease expired",
        ),
        EffectRecoveryEvent(
            EffectRecoveryEventType.EFFECT_REUSED,
            "effect-1",
            "already committed",
            "ok",
        ),
    ]
    state = RecoveryEventReplayer().replay(events)
    assert state["effect-1"].state == "committed"
    assert state["effect-1"].result == "ok"


def test_replay_preserves_latest_recovery_state() -> None:
    events = [
        EffectRecoveryEvent(EffectRecoveryEventType.EFFECT_RETRIED, "effect-1", "explicit failure", "ok"),
        EffectRecoveryEvent(EffectRecoveryEventType.EFFECT_RECOVERY_ABORTED, "effect-1", "owner changed"),
    ]
    state = RecoveryEventReplayer().replay(events)
    assert state["effect-1"].state == "aborted"
