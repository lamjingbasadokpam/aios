"""Standard runtime contract for an AIOS worker process."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass(frozen=True, slots=True)
class WorkerContext:
    agent_id: str
    model: str
    tools: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


class WorkerHandler(Protocol):
    async def handle(self, operation: str, payload: dict[str, Any]) -> dict[str, Any]: ...


class AgentWorkerRuntime:
    """Minimal protocol-independent worker runtime.

    Model execution, tool invocation, and transport are injected rather than
    hard-coded into the worker core.
    """

    def __init__(self, context: WorkerContext, handler: WorkerHandler) -> None:
        self.context = context
        self.handler = handler
        self.running = False

    async def start(self) -> None:
        self.running = True

    async def dispatch(self, operation: str, payload: dict[str, Any]) -> dict[str, Any]:
        if not self.running:
            raise RuntimeError("worker runtime is not running")
        return await self.handler.handle(operation, payload)

    async def stop(self) -> None:
        self.running = False
