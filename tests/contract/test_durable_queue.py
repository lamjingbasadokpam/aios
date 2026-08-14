from datetime import datetime, timedelta, timezone

import pytest

from aios.scheduler import DurableTaskQueue, QueueStatus, ScheduledTask, TaskPriority


def test_priority_and_lease_claim() -> None:
    now = datetime.now(timezone.utc)
    queue = DurableTaskQueue()
    low = ScheduledTask("low", lambda _: None, run_at=now, priority=TaskPriority.LOW)
    high = ScheduledTask("high", lambda _: None, run_at=now, priority=TaskPriority.HIGH)
    queue.enqueue(low)
    queue.enqueue(high)
    item = queue.claim("worker-a", lease_seconds=30, now=now)
    assert item.task.task_id == high.task_id
    assert item.status == QueueStatus.LEASED
    assert item.lease_owner == "worker-a"


def test_expired_lease_becomes_claimable_again() -> None:
    now = datetime.now(timezone.utc)
    queue = DurableTaskQueue()
    task = ScheduledTask("recover", lambda _: None, run_at=now)
    queue.enqueue(task)
    first = queue.claim("dead-worker", lease_seconds=1, now=now)
    assert first is not None
    recovered_at = now + timedelta(seconds=2)
    assert queue.recover_expired_leases(recovered_at) == 1
    second = queue.claim("worker-b", lease_seconds=30, now=recovered_at)
    assert second is not None
    assert second.lease_owner == "worker-b"
    assert second.attempts == 2


def test_only_lease_owner_can_complete() -> None:
    now = datetime.now(timezone.utc)
    queue = DurableTaskQueue()
    task = ScheduledTask("owned", lambda _: None, run_at=now)
    queue.enqueue(task)
    queue.claim("worker-a", now=now)
    with pytest.raises(RuntimeError):
        queue.complete(task.task_id, "worker-b")
    assert queue.complete(task.task_id, "worker-a").status == QueueStatus.COMPLETE
