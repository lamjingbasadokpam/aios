from aios.runtime.budget import ResourceUsage
from aios.runtime.overage import OverageAction, OverageGuard, OveragePolicy
from aios.runtime.settlement import SettlementResult, SettlementStatus


def _overage(tokens: int) -> SettlementResult:
    return SettlementResult(
        SettlementStatus.OVERAGE,
        ResourceUsage(tokens=500),
        ResourceUsage(tokens=500 + tokens),
        ResourceUsage(),
        ResourceUsage(tokens=tokens),
    )


def test_overage_stops_by_default() -> None:
    result = OverageGuard().evaluate(_overage(1))
    assert result.action == OverageAction.STOP


def test_overage_inside_grace_warns() -> None:
    guard = OverageGuard(OveragePolicy(action=OverageAction.STOP, grace_tokens=10))
    result = guard.evaluate(_overage(5))
    assert result.action == OverageAction.WARN


def test_non_overage_is_allowed() -> None:
    result = OverageGuard().evaluate(
        SettlementResult(SettlementStatus.SETTLED, ResourceUsage(), ResourceUsage(), ResourceUsage(), ResourceUsage())
    )
    assert result.action == OverageAction.ALLOW
