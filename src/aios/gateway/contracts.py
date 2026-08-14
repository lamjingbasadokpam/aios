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
