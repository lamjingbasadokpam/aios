"""Durable A2A outbox/inbox reference implementation."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from .contracts import A2AMessage, DeliveryStatus


@dataclass(frozen=True, slots=True)
class DeliveryRecord:
    message: A2AMessage
    status: DeliveryStatus = DeliveryStatus.QUEUED
    attempts: int = 0


class DurableMessageStore:
    def __init__(self) -> None:
        self._records: dict[UUID, DeliveryRecord] = {}
        self._inboxes: dict[UUID, list[UUID]] = {}

    def enqueue(self, message: A2AMessage) -> DeliveryRecord:
        record = DeliveryRecord(message)
        self._records[message.message_id] = record
        return record

    def claim(self, recipient: UUID) -> list[DeliveryRecord]:
        ids = self._inboxes.get(recipient, [])
        return [self._records[i] for i in ids if self._records[i].status == DeliveryStatus.QUEUED]

    def route(self, message: A2AMessage) -> DeliveryRecord:
        record = self._records.get(message.message_id) or self.enqueue(message)
        ids = self._inboxes.setdefault(message.recipient, [])
        if message.message_id not in ids:
            ids.append(message.message_id)
        return record

    def mark_delivered(self, message_id: UUID) -> DeliveryRecord:
        current = self._records[message_id]
        updated = DeliveryRecord(current.message, DeliveryStatus.DELIVERED, current.attempts + 1)
        self._records[message_id] = updated
        return updated

    def mark_failed(self, message_id: UUID) -> DeliveryRecord:
        current = self._records[message_id]
        updated = DeliveryRecord(current.message, DeliveryStatus.FAILED, current.attempts + 1)
        self._records[message_id] = updated
        return updated
