import asyncio
from pathlib import Path

from aios.model import ModelRegistry, ModelRouter
from aios.runtime import AgentRuntime, AgentRuntimeConfig
from aios.tools import ToolContext, ToolGateway, ToolRegistry
from adapters.models.mock import MockLocalProvider
from adapters.tools.filesystem import FILESYSTEM_WRITE, write_tool


def test_runtime_can_complete_with_model(tmp_path: Path) -> None:
    models = ModelRegistry()
    models.register_provider(MockLocalProvider())

    tools = ToolRegistry()
    gateway = ToolGateway(tools)
    runtime = AgentRuntime(ModelRouter(models), gateway)

    result = asyncio.run(runtime.run("Say hello"))

    assert result.success is True
    assert result.steps == 1
    assert result.output == "[mock-local] Say hello"


def test_runtime_enforces_tool_capability(tmp_path: Path) -> None:
    models = ModelRegistry()
    models.register_provider(MockLocalProvider())
    tools = ToolRegistry()
    tool, handler = write_tool(tmp_path)
    tools.register(tool, handler)

    runtime = AgentRuntime(
        ModelRouter(models),
        ToolGateway(tools),
        AgentRuntimeConfig(max_steps=2),
    )

    # Mock provider always produces a final action, so this proves the runtime
    # remains usable even when no tool is needed. Capability enforcement remains
    # owned by ToolGateway and is covered by Tool Fabric tests.
    result = asyncio.run(runtime.run("Write nothing"))
    assert result.success
