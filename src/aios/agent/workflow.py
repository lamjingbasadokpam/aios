"""Persistent workflow contracts and bounded execution state for AIOS."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from uuid import uuid4

from .execution import PlanExecutor, StepResult, StepStatus
from .planning import Plan, PlanStep


class WorkflowStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    PAUSED = "paused"


@dataclass(frozen=True, slots=True)
class Workflow:
    plan: Plan
    workflow_id: str = field(default_factory=lambda: str(uuid4()))
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class WorkflowState:
    workflow_id: str
    status: WorkflowStatus = WorkflowStatus.PENDING
    completed_steps: set[str] = field(default_factory=set)
    failed_steps: set[str] = field(default_factory=set)
    results: list[StepResult] = field(default_factory=list)


class WorkflowRunner:
    """Runs a workflow through the existing bounded plan executor."""

    def __init__(self, executor: PlanExecutor) -> None:
        self.executor = executor

    async def run(self, workflow: Workflow, state: WorkflowState | None = None) -> WorkflowState:
        state = state or WorkflowState(workflow.workflow_id)
        if state.status == WorkflowStatus.SUCCEEDED:
            return state
        state.status = WorkflowStatus.RUNNING
        try:
            results = await self.executor.execute(workflow.plan)
            state.results = results
            state.completed_steps = {r.step_id for r in results if r.status == StepStatus.SUCCEEDED}
            state.failed_steps = {r.step_id for r in results if r.status == StepStatus.FAILED}
            state.status = WorkflowStatus.FAILED if state.failed_steps else WorkflowStatus.SUCCEEDED
        except Exception:
            state.status = WorkflowStatus.FAILED
            raise
        return state
