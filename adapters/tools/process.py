"""Tool adapter exposing the bounded ProcessExecutor."""

from __future__ import annotations

from aios.execution import ExecutionRequest, ProcessExecutor
from aios.tools.contracts import Tool, ToolContext, ToolResult

PROCESS_EXECUTE = "process.execute"


def process_tool(executor: ProcessExecutor) -> tuple[Tool, object]:
    async def handler(arguments: dict, context: ToolContext) -> ToolResult:
        try:
            request = ExecutionRequest(
                executable=str(arguments["executable"]),
                arguments=tuple(str(value) for value in arguments.get("arguments", [])),
                working_directory=arguments.get("working_directory"),
                environment={str(k): str(v) for k, v in arguments.get("environment", {}).items()},
                timeout_seconds=float(arguments.get("timeout_seconds", 30.0)),
                max_output_bytes=int(arguments.get("max_output_bytes", 1_000_000)),
            )
            result = await executor.run(request)
            return ToolResult(
                success=result.success,
                output={"stdout": result.stdout, "stderr": result.stderr, "exit_code": result.exit_code},
                error=result.error,
                tool_id=PROCESS_EXECUTE,
            )
        except Exception as exc:
            return ToolResult(success=False, error=str(exc), tool_id=PROCESS_EXECUTE)

    return Tool(
        tool_id=PROCESS_EXECUTE,
        name="execute_process",
        description="Execute an allowlisted process inside the AIOS workspace.",
        input_schema={"type": "object", "required": ["executable"]},
        required_capabilities=frozenset({PROCESS_EXECUTE}),
        risk_level="high",
    ), handler
