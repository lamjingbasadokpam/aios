from uuid import uuid4

import pytest

from aios.gateway import AgentGateway, MessageEnvelope, TransportKind


def test_gateway_routes_to_registered_transport() -> None:
    gateway = AgentGateway()
    sender, recipient = uuid4(), uuid4()
    seen = []

    def handler(message):
        seen.append(message)
        return message

    gateway.register(TransportKind.IN_PROCESS, handler)
    message = MessageEnvelope(sender, recipient, {"hello": "world"}, TransportKind.IN_PROCESS)
    assert gateway.send(message) == message
    assert seen == [message]


def test_gateway_rejects_unregistered_transport() -> None:
    gateway = AgentGateway()
    message = MessageEnvelope(uuid4(), uuid4(), {}, TransportKind.HTTP)
    with pytest.raises(RuntimeError):
        gateway.send(message)
