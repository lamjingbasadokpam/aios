from datetime import datetime, timezone

from aios.runtime.events import RuntimeEvent
from aios.runtime.tracing import TraceBuilder


def test_trace_builder_reconstructs_completed_span() -> None:
    t0 = datetime(2026, 1, 1, tzinfo=timezone.utc)
    t1 = datetime(2026, 1, 1, 0, 0, 1, tzinfo=timezone.utc)
    events = [
        RuntimeEvent("tool.called", {"span_id": "s1", "tool": "search"}, occurred_at=t0, correlation_id="c1"),
        RuntimeEvent("tool.completed", {"span_id": "s1"}, occurred_at=t1, correlation_id="c1"),
        RuntimeEvent("tool.called", {"span_id": "other"}, occurred_at=t0, correlation_id="other"),
    ]
    trace = TraceBuilder().build(events, trace_id="t1", correlation_id="c1")
    assert trace.trace_id == "t1"
    assert len(trace.spans) == 1
    assert trace.spans[0].status == "succeeded"
    assert trace.spans[0].ended_at == t1
