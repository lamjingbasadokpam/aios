"""Runtime usage accounting derived from AIOS events."""

from __future__ import annotations

from dataclasses import dataclass

from .events import RuntimeEvent
from .budget import ResourceUsage


@dataclass(slots=True)
class UsageAccountant:
    """Accumulates explicitly reported resource usage; never guesses missing values."""

    usage: ResourceUsage = ResourceUsage()

    def observe(self, event: RuntimeEvent) -> ResourceUsage:
        u = self.usage
        tokens = event.payload.get("tokens", 0)
        latency = event.payload.get("latency_ms", 0)
        cost = event.payload.get("cost", 0)
        tool_calls = 1 if event.type == "tool.called" else 0
        retries = 1 if event.type == "tool.retry" else 0
        self.usage = ResourceUsage(
            tokens=u.tokens + (tokens if isinstance(tokens, int) and tokens >= 0 else 0),
            runtime_seconds=u.runtime_seconds + (latency / 1000 if isinstance(latency, (int, float)) and latency >= 0 else 0.0),
            tool_calls=u.tool_calls + tool_calls,
            retries=u.retries + retries,
            cost=u.cost + (float(cost) if isinstance(cost, (int, float)) and cost >= 0 else 0.0),
        )
        return self.usage
