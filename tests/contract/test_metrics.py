from aios.runtime.events import RuntimeEvent
from aios.runtime.metrics import RuntimeMetrics


def test_runtime_metrics_aggregate_events_errors_tokens_and_latency() -> None:
    metrics = RuntimeMetrics()
    metrics.observe(RuntimeEvent("tool.completed"))
    metrics.observe(RuntimeEvent("tool.failed"))
    metrics.observe(RuntimeEvent("model.completed", {"tokens": 120, "latency_ms": 250}))
    assert metrics.snapshot.counters["events.tool.completed"] == 1
    assert metrics.snapshot.counters["runtime.errors"] == 1
    assert metrics.snapshot.totals["model.tokens"] == 120
    assert metrics.snapshot.totals["model.latency_ms"] == 250
