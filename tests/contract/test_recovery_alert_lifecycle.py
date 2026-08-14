from aios.runtime.recovery_alert_events import RecoveryAlertEvent
from aios.runtime.recovery_alert_lifecycle import RecoveryAlertLifecycleTracker


def test_alert_stays_active_until_resolution() -> None:
    tracker = RecoveryAlertLifecycleTracker()
    alert = RecoveryAlertEvent("slow_recovery", "too slow", 42, 30)
    state = tracker.update([alert])
    assert state[("slow_recovery", 30)].active is True

    resolved = tracker.resolution_event(alert)
    state = tracker.update([alert, resolved])
    assert state[("slow_recovery", 30)].active is False


def test_same_condition_can_become_active_again_after_resolution() -> None:
    tracker = RecoveryAlertLifecycleTracker()
    alert = RecoveryAlertEvent("slow_recovery", "too slow", 42, 30)
    resolved = tracker.resolution_event(alert)
    again = RecoveryAlertEvent("slow_recovery", "too slow again", 45, 30)
    state = tracker.update([alert, resolved, again])
    assert state[("slow_recovery", 30)].active is True
    assert state[("slow_recovery", 30)].last_event is again
