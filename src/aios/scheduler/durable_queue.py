"""In-memory durable-queue contract with leases and crash recovery semantics."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import UUID

from .contracts import QueueItem, QueueStatus, ScheduledTask


class DurableTaskQueue:
    def __init__(self) -> None:
        self._items: dict[UUID, QueueItem] = {}

    def enqueue(self, task: ScheduledTask) -> QueueItem:
        item = QueueItem(task=task)
        self._items[task.task_id] = item
        return item

    def recover_expired_leases(self, now: datetime | None = None) -> int:
        now = now or datetime.now(timezone.utc)
        recovered = 0
        for task_id, item in list(self._items.items()):
            if item.status == QueueStatus.LEASED and item.lease_until and item.lease_until <= now:
                self._items[task_id] = QueueItem(task=item.task, enqueued_at=item.enqueued_at, attempts=item.attempts)
                recovered += 1
        return recovered

    def claim(self, worker_id: str, lease_seconds: float = 60.0, now: datetime | None = None) -> QueueItem | None:
        if lease_seconds <= 0:
            raise ValueError("lease_seconds must be > 0")
        now = now or datetime.now(timezone.utc)
        self.recover_expired_leases(now)
        ready = [
            item for item in self._items.values()
            if item.status == QueueStatus.READY and item.task.run_at <= now
        ]
        if not ready:
            return None
        item = sorted(ready, key=lambda x: (x.task.priority, x.task.run_at, x.enqueued_at))[0]
        claimed = QueueItem(
            task=item.task,
            enqueued_at=item.enqueued_at,
            status=QueueStatus.LEASED,
            lease_owner=worker_id,
            lease_until=now + timedelta(seconds=lease_seconds),
            attempts=item.attempts + 1,
        )
        self._items[item.task.task_id] = claimed
        return claimed

    def complete(self, task_id: UUID, worker_id: str) -> QueueItem:
        item = self._items[task_id]
        self._assert_owner(item, worker_id)
        completed = QueueItem(task=item.task, enqueued_at=item.enqueued_at, status=QueueStatus.COMPLETE, attempts=item.attempts)
        self._items[task_id] = completed
        return completed

    def fail(self, task_id: UUID, worker_id: str) -> QueueItem:
        item = self._items[task_id]
        self._assert_owner(item, worker_id)
        failed = QueueItem(task=item.task, enqueued_at=item.enqueued_at, status=QueueStatus.FAILED, attempts=item.attempts)
        self._items[task_id] = failed
        return failed

    def get(self, task_id: UUID) -> QueueItem | None:
        return self._items.get(task_id)

    @staticmethod
    def _assert_owner(item: QueueItem, worker_id: str) -> None:
        if item.status != QueueStatus.LEASED or item.lease_owner != worker_id:
            raise RuntimeError("Worker does not own the task lease")
