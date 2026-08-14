from uuid import uuid4

from aios.a2a.contracts import A2AMessage, DeliveryStatus, MessageKind
from aios.a2a.durable import DurableMessageStore


def test_durable_message_store_routes_and_delivers() -> None:
    sender, recipient = uuid4(), uuid4()
    message = A2AMessage(sender, recipient, MessageKind.REQUEST, {"task": "research"})
    store = DurableMessageStore()
    record = store.route(message)
    assert record.status == DeliveryStatus.QUEUED
    assert store.claim(recipient)[0].message.message_id == message.message_id
    delivered = store.mark_delivered(message.message_id)
    assert delivered.status == DeliveryStatus.DELIVERED
    assert store.claim(recipient) == []


def test_durable_message_store_marks_failed() -> None:
    message = A2AMessage(uuid4(), uuid4(), MessageKind.EVENT, {"ok": False})
    store = DurableMessageStore()
    store.route(message)
    failed = store.mark_failed(message.message_id)
    assert failed.status == DeliveryStatus.FAILED
    assert failed.attempts == 1
