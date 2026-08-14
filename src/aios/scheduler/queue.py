"""Priority queue for scheduled tasks."""

from __future__ import annotations

import heapq
import itertools
from datetime import datetime, timezone

from .contracts import QueueItem


class TaskQueue:
    def __init__(self) -> None:
        self._heap: list[tuple[datetime, int, int, QueueItem]] = []
        self._counter = itertools.count()

    def push(self, item: QueueItem) -> None:
        heapq.heappush(self._heap, (item.task.run_at, int(item.task.priority), next(self._counter), item))

    def pop_ready(self, now: datetime | None = None) -> QueueItem | None:
        now = now or datetime.now(timezone.utc)
        if not self._heap or self._heap[0][0] > now:
            return None
        return heapq.heappop(self._heap)[3]

    def __len__(self) -> int:
        return len(self._heap)
