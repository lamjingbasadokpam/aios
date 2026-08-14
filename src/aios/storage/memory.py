"""Reference in-memory implementation of the storage contract."""

from __future__ import annotations

from uuid import UUID

from .contracts import EventRecord, StoredExecution, StoredWorker


class InMemoryStorage:
    def __init__(self) -> None:
        self._executions: dict[UUID, StoredExecution] = {}
        self._workers: dict[UUID, StoredWorker] = {}
        self._events: list[EventRecord] = []

    async def save_execution(self, execution: StoredExecution) -> StoredExecution:
        self._executions[execution.execution_id] = execution
        return execution

    async def get_execution(self, execution_id: UUID) -> StoredExecution | None:
        return self._executions.get(execution_id)

    async def save_worker(self, worker: StoredWorker) -> StoredWorker:
        self._workers[worker.worker_id] = worker
        return worker

    async def get_worker(self, worker_id: UUID) -> StoredWorker | None:
        return self._workers.get(worker_id)

    async def append_event(self, event: EventRecord) -> EventRecord:
        if event.sequence <= 0:
            event = EventRecord(event.event_id, event.topic, dict(event.payload), event.occurred_at, len(self._events) + 1)
        self._events.append(event)
        return event

    async def events_since(self, sequence: int = 0) -> list[EventRecord]:
        return [event for event in self._events if event.sequence > sequence]
