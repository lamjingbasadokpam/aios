"""Small, provider-independent agent execution loop."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from typing import Any
from uuid import UUID

from aios.model import InferenceRequest, ModelRouter
from aios.recovery import RecoveryDecision, RecoveryHandler
from aios.recovery.classification import RecoveryClass, classify_failure
from aios.tools import ToolContext, ToolGateway, ToolResult


@dataclass(frozen=True, slots=True)
class AgentRuntimeConfig:
    max_steps: int = 8
    locality: str | None = "local"
    required_model_capabilities: frozenset[str] = frozenset()


@dataclass(slots=True)
class RuntimeResult:
    success: bool
    output: str | None = None
    error: str | None = None
    steps: int = 0
    tool_results: list[ToolResult] = field(default_factory=list)


class AgentRuntime:
    """Executes one task through a bounded observe/act loop."""

    def __init__(
        self,
        model_router: ModelRouter,
        tool_gateway: ToolGateway,
        config: AgentRuntimeConfig | None = None,
        recovery_handler: RecoveryHandler | None = None,
    ) -> None:
        self.model_router = model_router
        self.tool_gateway = tool_gateway
        self.config = config or AgentRuntimeConfig()
        self.recovery_handler = recovery_handler

    @staticmethod
    def _prompt(task: str, history: list[dict[str, Any]]) -> str:
        return (
            "You are an AIOS agent. Return exactly one JSON object.\n"
            "To finish: {\"action\":\"final\",\"answer\":\"...\"}\n"
            "To use a tool: {\"action\":\"tool\",\"tool_id\":\"...\",\"arguments\":{...}}\n"
            "Do not emit markdown or extra text.\n\n"
            f"TASK:\n{task}\n\n"
            f"HISTORY:\n{json.dumps(history, ensure_ascii=False)}"
        )

    @staticmethod
    def _parse_action(text: str) -> dict[str, Any]:
        try:
            action = json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Model returned invalid JSON: {exc}") from exc
        if not isinstance(action, dict) or action.get("action") not in {"final", "tool"}:
            raise ValueError("Model action must be 'final' or 'tool'")
        return action

    def _recover(self, exc: Exception, attempt: int) -> bool:
        if self.recovery_handler is None:
            return False
        if classify_failure(exc) is not RecoveryClass.TRANSIENT:
            return False
        return self.recovery_handler.decide(exc, attempt) is RecoveryDecision.RETRY

    async def run(
        self,
        task: str,
        *,
        task_id: UUID | None = None,
        agent_id: UUID | None = None,
        granted_capabilities: frozenset[str] = frozenset(),
    ) -> RuntimeResult:
        history: list[dict[str, Any]] = []
        tool_results: list[ToolResult] = []

        for step in range(1, self.config.max_steps + 1):
            attempt = 1
            while True:
                try:
                    request = InferenceRequest(
                        prompt=self._prompt(task, history),
                        metadata={"runtime_step": step, "recovery_attempt": attempt},
                    )
                    response = await self.model_router.generate(
                        request,
                        locality=self.config.locality,
                        require=set(self.config.required_model_capabilities),
                    )
                    action = self._parse_action(response.text)
                except Exception as exc:
                    if self._recover(exc, attempt):
                        attempt += 1
                        continue
                    return RuntimeResult(False, error=str(exc), steps=step - 1, tool_results=tool_results)

                if action["action"] == "final":
                    answer = str(action.get("answer", ""))
                    return RuntimeResult(True, output=answer, steps=step, tool_results=tool_results)

                tool_id = action.get("tool_id")
                arguments = action.get("arguments", {})
                if not isinstance(tool_id, str) or not isinstance(arguments, dict):
                    exc = ValueError("Invalid tool action")
                    if self._recover(exc, attempt):
                        attempt += 1
                        continue
                    return RuntimeResult(False, error=str(exc), steps=step, tool_results=tool_results)

                try:
                    result = await self.tool_gateway.invoke(
                        tool_id,
                        arguments,
                        ToolContext(
                            task_id=task_id,
                            agent_id=agent_id,
                            granted_capabilities=granted_capabilities,
                        ),
                    )
                except Exception as exc:
                    result = ToolResult(success=False, error=str(exc), tool_id=tool_id)

                if not result.success:
                    exc = RuntimeError(result.error or f"Tool '{tool_id}' failed")
                    history.append({
                        "step": step,
                        "attempt": attempt,
                        "tool": tool_id,
                        "success": False,
                        "output": result.output,
                        "error": result.error,
                    })
                    if self._recover(exc, attempt):
                        attempt += 1
                        continue
                    tool_results.append(result)
                    return RuntimeResult(False, error=result.error, steps=step, tool_results=tool_results)

                tool_results.append(result)
                history.append({
                    "step": step,
                    "attempt": attempt,
                    "tool": tool_id,
                    "success": result.success,
                    "output": result.output,
                    "error": result.error,
                })
                break

        return RuntimeResult(
            False,
            error=f"Maximum agent steps exceeded ({self.config.max_steps})",
            steps=self.config.max_steps,
            tool_results=tool_results,
        )
