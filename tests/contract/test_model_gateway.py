import pytest

from aios.model.gateway import ModelGateway, ModelRequest, ModelResponse


class FakeModel:
    async def generate(self, request):
        return ModelResponse(request.model, "hello", "stop", {"input_tokens": 1})


@pytest.mark.asyncio
async def test_gateway_routes_to_registered_provider() -> None:
    gateway = ModelGateway()
    gateway.register("local", FakeModel())
    response = await gateway.generate("local", ModelRequest("qwen", ({"role": "user", "content": "hi"},)))
    assert response.content == "hello"
    assert response.model == "qwen"


@pytest.mark.asyncio
async def test_gateway_rejects_unknown_provider() -> None:
    gateway = ModelGateway()
    with pytest.raises(LookupError):
        await gateway.generate("missing", ModelRequest("qwen", ()))
