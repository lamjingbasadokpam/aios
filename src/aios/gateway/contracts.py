"""Transport-neutral gateway contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4


class TransportKind(StrEnum):
    IN_PROCESS = "in_process"
    IPC = "ipc"
    HTTP = "http"
    WEBSOCKET = "websocket"


@dataclass(frozen=True, slots=True)
class MessageEnvelope:
    sender: UUID
    recipient: UUID
    payload: dict[str, Any]
    transport: TransportKind
    request_id: UUID = field(default_factory=uuid4)
    correlation_id: UUID | None = None
    headers: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "sender": str(self.sender),
            "recipient": str(self.recipient),
            "payload": self.payload,
            "transport": self.transport.value,
            "request_id": str(self.request_id),
            "correlation_id": str(self.correlation_id) if self.correlation_id else None,
            "headers": self.headers,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MessageEnvelope":
        return cls(
            sender=UUID(data["sender"]),
            recipient=UUID(data["recipient"]),
            payload=dict(data.get("payload", {})),
            transport=TransportKind(data["transport"]),
            request_id=UUID(data["request_id"]),
            correlation_id=UUID(data["correlation_id"]) if data.get("correlation_id") else None,
            headers=dict(data.get("headers", {})),
        )
