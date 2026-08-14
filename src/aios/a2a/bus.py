"""In-process reference A2A message bus."""

from __future__ import annotations

from collections import defaultdict, deque
from uuid import UUID

from .contracts import A2AMessage, DeliveryStatus


class AgentMessageBus:
    def __init__(self) -> None:
        self._inboxes: dict[UUID, deque[A2AMessage]] = defaultdict(deque)
        self._status: dict[UUID, DeliveryStatus] = {}

    def register(self, agent_id: UUID) -> None:
        self._inboxes.setdefault(agent_id, deque())

    def send(self, message: A2AMessage) -> DeliveryStatus:
        if message.recipient not in self._inboxes:
            self._status[message.message_id] = DeliveryStatus.FAILED
            return DeliveryStatus.FAILED
        self._inboxes[message.recipient].append(message)
        self._status[message.message_id] = DeliveryStatus.QUEUED
        return DeliveryStatus.QUEUED

    def receive(self, agent_id: UUID) -> A2AMessage | None:
        inbox = self._inboxes.get(agent_id)
        if not inbox:
            return None
        message = inbox.popleft()
        self._status[message.message_id] = DeliveryStatus.DELIVERED
        return message

    def status(self, message_id: UUID) -> DeliveryStatus | None:
        return self._status.get(message_id)
