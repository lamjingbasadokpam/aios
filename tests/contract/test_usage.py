from aios.runtime.events import RuntimeEvent
from aios.runtime.usage import UsageAccountant


def test_usage_accountant_accumulates_explicit_runtime_usage() -> None:
    accountant = UsageAccountant()
    accountant.observe(RuntimeEvent("model.completed", {"tokens": 100, "latency_ms": 500, "cost": 0.2}))
    usage = accountant.observe(RuntimeEvent("tool.called"))
    assert usage.tokens == 100
    assert usage.runtime_seconds == 0.5
    assert usage.tool_calls == 1
    assert usage.cost == 0.2


def test_usage_accountant_ignores_missing_or_invalid_telemetry() -> None:
    usage = UsageAccountant().observe(RuntimeEvent("model.completed", {"tokens": -10, "cost": "unknown"}))
    assert usage.tokens == 0
    assert usage.cost == 0
