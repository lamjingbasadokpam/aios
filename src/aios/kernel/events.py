"""Minimal synchronous event bus for Kernel V0."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class Event:
    type: str
    source: str
    event_id: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    actor_id: UUID | None = None
    task_id: UUID | None = None
    correlation_id: UUID | None = None
    payload: dict[str, Any] = field(default_factory=dict)
    severity: str = "info"


Subscriber = Callable[[Event], None]


class EventBus:
    def __init__(self) -> None:
        self._subscribers: dict[str, list[Subscriber]] = {}
        self._history: list[Event] = []

    def subscribe(self, event_type: str, subscriber: Subscriber) -> None:
        self._subscribers.setdefault(event_type, []).append(subscriber)

    def publish(self, event: Event) -> None:
        self._history.append(event)
        for subscriber in self._subscribers.get(event.type, []):
            subscriber(event)
        for subscriber in self._subscribers.get("*", []):
            subscriber(event)

    def history(self) -> list[Event]:
        return list(self._history)
