"""Provider-neutral runtime metrics derived from AIOS events."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .events import RuntimeEvent


@dataclass(slots=True)
class MetricSnapshot:
    counters: dict[str, int] = field(default_factory=dict)
    gauges: dict[str, float] = field(default_factory=dict)
    totals: dict[str, float] = field(default_factory=dict)

    def increment(self, name: str, value: int = 1) -> None:
        self.counters[name] = self.counters.get(name, 0) + value

    def add_total(self, name: str, value: float) -> None:
        self.totals[name] = self.totals.get(name, 0.0) + value


class RuntimeMetrics:
    """Aggregates stable runtime signals without coupling to a metrics vendor."""

    def __init__(self) -> None:
        self.snapshot = MetricSnapshot()

    def observe(self, event: RuntimeEvent) -> None:
        self.snapshot.increment(f"events.{event.type}")
        if event.type.endswith(".failed"):
            self.snapshot.increment("runtime.errors")
        if event.type == "model.completed":
            tokens = event.payload.get("tokens")
            if isinstance(tokens, (int, float)):
                self.snapshot.add_total("model.tokens", float(tokens))
            latency_ms = event.payload.get("latency_ms")
            if isinstance(latency_ms, (int, float)):
                self.snapshot.add_total("model.latency_ms", float(latency_ms))
