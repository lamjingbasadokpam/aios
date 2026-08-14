from aios.runtime.effect_recovery_events import EffectRecoveryEvent, EffectRecoveryEventType
from aios.runtime.recovery_event_store import RuntimeRecoveryEventStore


def test_recovery_event_is_mapped_to_runtime_event_store() -> None:
    persisted = []
    store = RuntimeRecoveryEventStore(lambda event_type, payload: persisted.append((event_type, payload)))

    store.emit(
        EffectRecoveryEvent(
            EffectRecoveryEventType.EFFECT_REUSED,
            "effect-1",
            "already committed",
            "ok",
        )
    )

    assert persisted == [
        (
            "effect_reused",
            {"effect_key": "effect-1", "reason": "already committed", "result": "ok"},
        )
    ]
