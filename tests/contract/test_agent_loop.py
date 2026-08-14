import pytest

from aios.agent.loop import AgentLoop, AgentStep
from aios.model.gateway import ModelGateway, ModelResponse
from aios.tools.fabric import ToolFabric, ToolResponse


class Model:
    async def generate(self, request):
        return ModelResponse(request.model, "call tool")


class Parser:
    def parse(self, response):
        return AgentStep("tool_call", tool="echo", arguments={"value": "ok"})


class Tool:
    async def execute(self, request):
        return ToolResponse(request.tool, True, "tool-result")


@pytest.mark.asyncio
async def test_loop_executes_tool_then_requires_next_model_decision() -> None:
    gateway = ModelGateway()
    gateway.register("local", Model())
    tools = ToolFabric()
    tools.register("echo", Tool())
    loop = AgentLoop(gateway, tools, Parser())
    with pytest.raises(RuntimeError, match="max_steps"):
        await loop.run(provider="local", model="qwen", messages=[], max_steps=1)
