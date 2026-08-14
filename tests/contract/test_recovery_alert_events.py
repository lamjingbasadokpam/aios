from aios.runtime.recovery_alert_events import RecoveryAlertEvent, RecoveryAlertEventSink
from aios.runtime.recovery_alerts import RecoveryAlert


def test_alert_is_converted_to_durable_event() -> None:
    alert = RecoveryAlert("slow_recovery", "too slow", 42.0, 30.0)
    event = RecoveryAlertEvent.from_alert(alert)
    assert event.code == "slow_recovery"
    assert event.value == 42.0
    assert event.threshold == 30.0


def test_alert_event_sink_persists_structured_payload() -> None:
    seen = []
    sink = RecoveryAlertEventSink(lambda event_type, payload: seen.append((event_type, payload)))
    sink.emit(RecoveryAlertEvent("recovery_failures", "too many", 5, 2))
    assert seen == [
        (
            "recovery_alert",
            {"code": "recovery_failures", "message": "too many", "value": 5, "threshold": 2},
        )
    ]
