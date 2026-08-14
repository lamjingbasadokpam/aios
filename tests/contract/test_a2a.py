from uuid import uuid4

from aios.a2a import A2AMessage, AgentMessageBus, DeliveryStatus, MessageKind


def test_a2a_send_receive_and_correlation() -> None:
    sender, recipient = uuid4(), uuid4()
    bus = AgentMessageBus()
    bus.register(sender)
    bus.register(recipient)
    message = A2AMessage(sender, recipient, MessageKind.REQUEST, {"task": "research"})
    assert bus.send(message) == DeliveryStatus.QUEUED
    assert bus.status(message.message_id) == DeliveryStatus.QUEUED
    received = bus.receive(recipient)
    assert received == message
    assert bus.status(message.message_id) == DeliveryStatus.DELIVERED


def test_a2a_unknown_recipient_fails() -> None:
    bus = AgentMessageBus()
    message = A2AMessage(uuid4(), uuid4(), MessageKind.EVENT, {})
    assert bus.send(message) == DeliveryStatus.FAILED
    assert bus.status(message.message_id) == DeliveryStatus.FAILED
