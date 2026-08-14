"""Provider-neutral runtime event bus for AIOS."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Awaitable, Callable
from uuid import uuid4


@dataclass(frozen=True, slots=True)
class RuntimeEvent:
    type: str
    payload: dict[str, Any] = field(default_factory=dict)
    event_id: str = field(default_factory=lambda: str(uuid4()))
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    correlation_id: str | None = None


EventHandler = Callable[[RuntimeEvent], Awaitable[None]]


class EventBus:
    """In-process async pub/sub bus with isolated handler failures."""

    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandler]] = {}

    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        self._handlers.setdefault(event_type, []).append(handler)

    async def publish(self, event: RuntimeEvent) -> None:
        handlers = [*self._handlers.get(event.type, []), *self._handlers.get("*", [])]
        if not handlers:
            return
        results = await asyncio.gather(*(handler(event) for handler in handlers), return_exceptions=True)
        errors = [result for result in results if isinstance(result, Exception)]
        if errors:
            raise RuntimeError(f"{len(errors)} event handler(s) failed") from errors[0]
