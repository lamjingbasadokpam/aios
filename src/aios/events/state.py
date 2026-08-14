"""Durable-ready execution state contract with an in-memory V0 backend."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class ExecutionState:
    execution_id: UUID
    status: str
    step: int = 0
    checkpoint: dict[str, Any] = field(default_factory=dict)
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    version: int = 0


class StateStore:
    """Optimistic-versioned state store; production backends can implement this contract."""

    def __init__(self) -> None:
        self._states: dict[UUID, ExecutionState] = {}

    def get(self, execution_id: UUID) -> ExecutionState | None:
        return self._states.get(execution_id)

    def put(self, state: ExecutionState, expected_version: int | None = None) -> ExecutionState:
        current = self._states.get(state.execution_id)
        if expected_version is not None:
            actual = current.version if current else 0
            if actual != expected_version:
                raise RuntimeError(f"State version conflict: expected {expected_version}, got {actual}")
        version = (current.version + 1) if current else 1
        stored = ExecutionState(
            execution_id=state.execution_id,
            status=state.status,
            step=state.step,
            checkpoint=dict(state.checkpoint),
            updated_at=datetime.now(timezone.utc),
            version=version,
        )
        self._states[state.execution_id] = stored
        return stored
