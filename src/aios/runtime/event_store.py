"""Append-only event persistence and replay boundary for AIOS."""

from __future__ import annotations

import inspect
from dataclasses import dataclass, field
from typing import Protocol

from .events import RuntimeEvent


class EventStore(Protocol):
    async def append(self, event: RuntimeEvent) -> None: ...
    async def list(self, *, correlation_id: str | None = None, event_type: str | None = None) -> list[RuntimeEvent]: ...
    async def replay(self, handler, *, correlation_id: str | None = None, event_type: str | None = None) -> None: ...


@dataclass(slots=True)
class InMemoryEventStore:
    _events: list[RuntimeEvent] = field(default_factory=list)

    async def append(self, event: RuntimeEvent) -> None:
        self._events.append(event)

    async def list(self, *, correlation_id: str | None = None, event_type: str | None = None) -> list[RuntimeEvent]:
        return [
            event for event in self._events
            if (correlation_id is None or event.correlation_id == correlation_id)
            and (event_type is None or event.type == event_type)
        ]

    async def replay(self, handler, *, correlation_id: str | None = None, event_type: str | None = None) -> None:
        for event in await self.list(correlation_id=correlation_id, event_type=event_type):
            result = handler(event)
            if inspect.isawaitable(result):
                await result


class DurableEventStoreUnavailable(RuntimeError):
    """Raised when a durable provider is requested but not configured."""
