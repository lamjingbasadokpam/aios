import pytest

from aios.tools.fabric import ToolFabric, ToolRequest, ToolResponse


class FakeTool:
    async def execute(self, request):
        return ToolResponse(request.tool, True, {"echo": request.arguments})


@pytest.mark.asyncio
async def test_fabric_routes_registered_tool() -> None:
    fabric = ToolFabric()
    fabric.register("echo", FakeTool())
    assert fabric.list_tools() == ("echo",)
    response = await fabric.execute(ToolRequest("echo", {"x": 1}))
    assert response.success is True
    assert response.result == {"echo": {"x": 1}}


@pytest.mark.asyncio
async def test_fabric_rejects_unknown_tool() -> None:
    fabric = ToolFabric()
    with pytest.raises(LookupError):
        await fabric.execute(ToolRequest("missing"))
