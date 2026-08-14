"""Small async in-process event bus with durable-friendly event contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Awaitable, Callable
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class Event:
    topic: str
    payload: dict[str, Any]
    event_id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    correlation_id: UUID | None = None
    causation_id: UUID | None = None


Subscriber = Callable[[Event], Awaitable[None]]


class EventBus:
    def __init__(self) -> None:
        self._subscribers: dict[str, list[Subscriber]] = {}

    def subscribe(self, topic: str, subscriber: Subscriber) -> None:
        self._subscribers.setdefault(topic, []).append(subscriber)

    async def publish(self, event: Event) -> None:
        subscribers = [*self._subscribers.get(event.topic, []), *self._subscribers.get("*", [])]
        for subscriber in subscribers:
            await subscriber(event)
