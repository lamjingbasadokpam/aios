from aios.runtime.recovery_alert_routing import RecoveryAlertRoute, RecoveryAlertRouter
from aios.runtime.recovery_alerts import RecoveryAlert


def test_alert_routes_to_matching_sink() -> None:
    seen = []
    router = RecoveryAlertRouter(
        [RecoveryAlertRoute("slow_recovery", "metrics")],
        {"metrics": seen.append},
    )
    alert = RecoveryAlert("slow_recovery", "too slow", 42, 30)
    assert router.route(alert) == ["metrics"]
    assert seen == [alert]


def test_wildcard_route_supports_general_sink() -> None:
    seen = []
    router = RecoveryAlertRouter(
        [RecoveryAlertRoute("*", "audit")],
        {"audit": seen.append},
    )
    alert = RecoveryAlert("recovery_failures", "too many", 5, 2)
    assert router.route(alert) == ["audit"]
    assert seen == [alert]
