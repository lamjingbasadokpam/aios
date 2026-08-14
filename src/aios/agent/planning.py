"""Provider-neutral planning contracts for AIOS agents."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol
from uuid import uuid4


@dataclass(frozen=True, slots=True)
class PlanStep:
    description: str
    step_id: str = field(default_factory=lambda: str(uuid4()))
    depends_on: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Plan:
    goal: str
    steps: tuple[PlanStep, ...]
    plan_id: str = field(default_factory=lambda: str(uuid4()))


class Planner(Protocol):
    async def create_plan(self, goal: str, context: str = "") -> Plan: ...


class StaticPlanner:
    """Small deterministic planner for local tests and orchestration contracts."""

    async def create_plan(self, goal: str, context: str = "") -> Plan:
        if not goal.strip():
            raise ValueError("goal is required")
        return Plan(goal=goal, steps=(PlanStep(description=goal),))


class PlanValidator:
    @staticmethod
    def validate(plan: Plan) -> None:
        ids = {step.step_id for step in plan.steps}
        for step in plan.steps:
            if any(dependency not in ids for dependency in step.depends_on):
                raise ValueError(f"Unknown dependency in step {step.step_id}")
