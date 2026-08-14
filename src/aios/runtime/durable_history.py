"""Durable lifecycle history facade for AIOS runtime events."""

from __future__ import annotations

from dataclasses import dataclass

from .events import RuntimeEvent


@dataclass(slots=True)
class DurableLifecycleHistory:
    """Append-only run history backed by an injected event store."""

    event_store: object

    async def append(self, event: RuntimeEvent) -> None:
        append = getattr(self.event_store, "append", None)
        if append is None:
            raise TypeError("event_store must provide append(event)")
        result = append(event)
        if hasattr(result, "__await__"):
            await result

    async def history(self, run_id: str) -> list[RuntimeEvent]:
        reader = getattr(self.event_store, "for_run", None)
        if reader is None:
            reader = getattr(self.event_store, "get_for_run", None)
        if reader is None:
            raise TypeError("event_store must provide for_run(run_id) or get_for_run(run_id)")
        result = reader(run_id)
        if hasattr(result, "__await__"):
            result = await result
        return list(result)
