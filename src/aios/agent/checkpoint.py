"""Checkpoint persistence boundary for AIOS workflows."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Protocol
import json

from .workflow import WorkflowState, WorkflowStatus


class CheckpointStore(Protocol):
    async def save(self, state: WorkflowState) -> None: ...
    async def load(self, workflow_id: str) -> WorkflowState | None: ...


@dataclass(slots=True)
class InMemoryCheckpointStore:
    _data: dict[str, str] | None = None

    def __post_init__(self) -> None:
        if self._data is None:
            self._data = {}

    async def save(self, state: WorkflowState) -> None:
        self._data[state.workflow_id] = json.dumps({
            "workflow_id": state.workflow_id,
            "status": state.status.value,
            "completed_steps": sorted(state.completed_steps),
            "failed_steps": sorted(state.failed_steps),
            "results": [
                {"step_id": r.step_id, "status": r.status.value, "output": r.output,
                 "error": r.error, "attempts": r.attempts}
                for r in state.results
            ],
        }, default=str)

    async def load(self, workflow_id: str) -> WorkflowState | None:
        raw = self._data.get(workflow_id)
        if raw is None:
            return None
        payload = json.loads(raw)
        from .execution import StepResult, StepStatus
        return WorkflowState(
            workflow_id=payload["workflow_id"],
            status=WorkflowStatus(payload["status"]),
            completed_steps=set(payload["completed_steps"]),
            failed_steps=set(payload["failed_steps"]),
            results=[StepResult(r["step_id"], StepStatus(r["status"]), r["output"], r["error"], r["attempts"]) for r in payload["results"]],
        )
