"""Agent gateway routing abstraction."""

from __future__ import annotations

from collections.abc import Callable

from .contracts import MessageEnvelope, TransportKind


TransportHandler = Callable[[MessageEnvelope], MessageEnvelope | None]


class AgentGateway:
    def __init__(self) -> None:
        self._handlers: dict[TransportKind, TransportHandler] = {}

    def register(self, transport: TransportKind, handler: TransportHandler) -> None:
        self._handlers[transport] = handler

    def send(self, envelope: MessageEnvelope) -> MessageEnvelope | None:
        handler = self._handlers.get(envelope.transport)
        if handler is None:
            raise RuntimeError(f"No gateway transport registered: {envelope.transport}")
        return handler(envelope)
