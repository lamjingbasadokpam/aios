"""Bounded plan execution and orchestration for AIOS."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Protocol

from .planning import Plan, PlanStep, PlanValidator


class StepStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass(frozen=True, slots=True)
class StepResult:
    step_id: str
    status: StepStatus
    output: Any = None
    error: str | None = None
    attempts: int = 1


class StepExecutor(Protocol):
    async def execute(self, step: PlanStep) -> Any: ...


class PlanExecutor:
    """Executes dependency-ordered plan steps with bounded retries."""

    def __init__(self, step_executor: StepExecutor, *, max_steps: int = 32, max_retries: int = 0) -> None:
        if max_steps <= 0 or max_retries < 0:
            raise ValueError("max_steps must be positive and max_retries non-negative")
        self.step_executor = step_executor
        self.max_steps = max_steps
        self.max_retries = max_retries

    async def execute(self, plan: Plan) -> list[StepResult]:
        PlanValidator.validate(plan)
        if len(plan.steps) > self.max_steps:
            raise ValueError("plan exceeds max_steps")
        results: dict[str, StepResult] = {}
        remaining = list(plan.steps)
        while remaining:
            progressed = False
            for step in list(remaining):
                dependencies = [results[dep] for dep in step.depends_on]
                if any(dep.status != StepStatus.SUCCEEDED for dep in dependencies):
                    if any(dep.status == StepStatus.FAILED for dep in dependencies):
                        results[step.step_id] = StepResult(step.step_id, StepStatus.SKIPPED, error="dependency failed")
                        remaining.remove(step)
                        progressed = True
                    continue
                remaining.remove(step)
                progressed = True
                attempts = 0
                while attempts <= self.max_retries:
                    attempts += 1
                    try:
                        output = await self.step_executor.execute(step)
                        results[step.step_id] = StepResult(step.step_id, StepStatus.SUCCEEDED, output, attempts=attempts)
                        break
                    except Exception as exc:
                        if attempts > self.max_retries:
                            results[step.step_id] = StepResult(step.step_id, StepStatus.FAILED, error=str(exc), attempts=attempts)
            if not progressed:
                raise ValueError("plan contains unresolved dependencies")
        return [results[step.step_id] for step in plan.steps]
