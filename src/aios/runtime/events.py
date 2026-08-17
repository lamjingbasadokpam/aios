"""Provider-neutral runtime event bus for AIOS."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Awaitable, Callable
from uuid import uuid4


@dataclass(frozen=True, slots=True, init=False)
class RuntimeEvent:
    type: str
    payload: dict[str, Any]
    event_id: str
    occurred_at: datetime
    correlation_id: str | None

    def __init__(self, type: str, payload: Any = None, event_id: str | None = None,
                 occurred_at: datetime | str | None = None, correlation_id: str | None = None,
                 *legacy: Any, timestamp: datetime | str | None = None,
                 source: str | None = None, run_id: str | None = None) -> None:
        if isinstance(payload, str) and legacy:
            legacy_payload = legacy[0] if isinstance(legacy[0], dict) else {}
            actual_event_id = type
            actual_type = payload
            actual_time = event_id
            actual_source = occurred_at
            actual_run_id = correlation_id
            actual_correlation = None
            actual_payload = dict(legacy_payload)
        else:
            actual_event_id = event_id or str(uuid4())
            actual_type = type
            actual_time = timestamp if timestamp is not None else occurred_at
            actual_source = source
            actual_run_id = run_id
            actual_correlation = correlation_id
            actual_payload = dict(payload or {}) if isinstance(payload, dict) else {}

        if isinstance(actual_time, str):
            try:
                actual_time = datetime.fromisoformat(actual_time.replace("Z", "+00:00"))
            except ValueError:
                # Older contracts used opaque timestamp strings such as "t".
                # Preserve event construction while normalizing to a real UTC time.
                actual_time = datetime.now(timezone.utc)
        if actual_time is None:
            actual_time = datetime.now(timezone.utc)
        if actual_time.tzinfo is None:
            actual_time = actual_time.replace(tzinfo=timezone.utc)
        if actual_source is not None:
            actual_payload.setdefault("_source", str(actual_source))
        if actual_run_id is not None:
            actual_payload.setdefault("_run_id", str(actual_run_id))

        object.__setattr__(self, "type", str(actual_type))
        object.__setattr__(self, "payload", actual_payload)
        object.__setattr__(self, "event_id", str(actual_event_id))
        object.__setattr__(self, "occurred_at", actual_time)
        object.__setattr__(self, "correlation_id", actual_correlation)

    @property
    def timestamp(self) -> datetime:
        return self.occurred_at

    @property
    def source(self) -> str | None:
        value = self.payload.get("_source")
        return str(value) if value is not None else None

    @property
    def run_id(self) -> str | None:
        value = self.payload.get("_run_id")
        return str(value) if value is not None else None


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
