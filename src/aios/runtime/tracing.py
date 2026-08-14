"""Execution tracing built on AIOS runtime events."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .events import RuntimeEvent


@dataclass(frozen=True, slots=True)
class TraceSpan:
    span_id: str
    name: str
    started_at: datetime
    ended_at: datetime | None = None
    attributes: dict[str, Any] = field(default_factory=dict)
    status: str = "running"


@dataclass(frozen=True, slots=True)
class ExecutionTrace:
    trace_id: str
    correlation_id: str
    spans: tuple[TraceSpan, ...]


class TraceBuilder:
    """Builds a deterministic trace projection from runtime events."""

    def build(self, events: list[RuntimeEvent], *, trace_id: str, correlation_id: str) -> ExecutionTrace:
        relevant = [e for e in events if e.correlation_id == correlation_id]
        starts: dict[str, RuntimeEvent] = {}
        spans: list[TraceSpan] = []
        for event in relevant:
            span_id = str(event.payload.get("span_id", event.event_id))
            if event.type.endswith(".started") or event.type.endswith(".called"):
                starts[span_id] = event
                spans.append(TraceSpan(span_id, event.type, event.occurred_at, attributes=dict(event.payload)))
            elif event.type.endswith(".completed") or event.type.endswith(".failed"):
                start = starts.get(span_id)
                if start is None:
                    continue
                status = "failed" if event.type.endswith(".failed") else "succeeded"
                spans = [
                    TraceSpan(s.span_id, s.name, s.started_at, event.occurred_at, s.attributes, status)
                    if s.span_id == span_id else s for s in spans
                ]
        return ExecutionTrace(trace_id, correlation_id, tuple(spans))
