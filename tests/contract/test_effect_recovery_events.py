from aios.runtime.effect_recovery_events import (
    EffectRecoveryEvent,
    EffectRecoveryEventSink,
    EffectRecoveryEventType,
)


def test_recovery_events_are_emitted_to_sink() -> None:
    events = []
    sink = EffectRecoveryEventSink(events.append)
    event = EffectRecoveryEvent(
        EffectRecoveryEventType.EFFECT_RECONCILIATION_REQUIRED,
        "effect-1",
        "lease expired",
    )
    sink.emit(event)
    assert events == [event]


def test_recovery_event_preserves_result() -> None:
    events = []
    sink = EffectRecoveryEventSink(events.append)
    event = EffectRecoveryEvent(
        EffectRecoveryEventType.EFFECT_REUSED,
        "effect-1",
        "already committed",
        "ok",
    )
    sink.emit(event)
    assert events[0].result == "ok"
