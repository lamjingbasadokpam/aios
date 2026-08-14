from uuid import uuid4

from aios.gateway.contracts import MessageEnvelope, TransportKind


def test_message_envelope_round_trips() -> None:
    message = MessageEnvelope(uuid4(), uuid4(), {"task": "ping"}, TransportKind.IPC)
    assert MessageEnvelope.from_dict(message.to_dict()) == message
