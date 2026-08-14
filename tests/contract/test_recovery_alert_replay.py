from aios.runtime.recovery_alert_events import RecoveryAlertEvent
from aios.runtime.recovery_alert_replay import RecoveryAlertReplayer


def test_replay_deduplicates_same_alert_identity() -> None:
    events = [
        RecoveryAlertEvent("slow_recovery", "too slow", 42, 30),
        RecoveryAlertEvent("slow_recovery", "too slow again", 50, 30),
        RecoveryAlertEvent("recovery_failures", "too many", 5, 2),
    ]
    replayed = RecoveryAlertReplayer().replay(events)
    assert replayed == [events[0], events[2]]


def test_different_thresholds_are_distinct_alert_identities() -> None:
    events = [
        RecoveryAlertEvent("slow_recovery", "slow", 42, 30),
        RecoveryAlertEvent("slow_recovery", "slow", 42, 60),
    ]
    assert RecoveryAlertReplayer().replay(events) == events
