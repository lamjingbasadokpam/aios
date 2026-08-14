"""Typed A2A message contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from uuid import UUID, uuid4
from typing import Any


class MessageKind(StrEnum):
    REQUEST = "request"
    RESPONSE = "response"
    EVENT = "event"
    DELEGATION = "delegation"


class DeliveryStatus(StrEnum):
    QUEUED = "queued"
    DELIVERED = "delivered"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class A2AMessage:
    sender: UUID
    recipient: UUID
    kind: MessageKind
    payload: dict[str, Any]
    correlation_id: UUID | None = None
    message_id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
