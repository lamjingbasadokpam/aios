import asyncio

from aios.model import InferenceRequest, ModelRegistry, ModelRouter
from adapters.models.mock import MockLocalProvider


def test_model_registry_and_local_routing() -> None:
    registry = ModelRegistry()
    registry.register_provider(MockLocalProvider())
    router = ModelRouter(registry)

    response = asyncio.run(router.generate(InferenceRequest(prompt="hello"), locality="local"))

    assert response.provider == "mock-local"
    assert response.model_id == "mock-local/default"
    assert response.text == "[mock-local] hello"


def test_requested_model_is_respected() -> None:
    registry = ModelRegistry()
    registry.register_provider(MockLocalProvider())
    router = ModelRouter(registry)

    request = InferenceRequest(prompt="hello", model_id="mock-local/default")
    response = asyncio.run(router.generate(request))

    assert response.model_id == request.model_id
