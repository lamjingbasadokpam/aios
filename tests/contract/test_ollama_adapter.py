from aios.model import ModelRegistry
from adapters.models.ollama import OllamaProvider


def test_ollama_provider_is_local() -> None:
    provider = OllamaProvider()
    assert provider.provider_id == "ollama"
    assert provider.base_url == "http://127.0.0.1:11434"


def test_unavailable_ollama_is_non_fatal() -> None:
    provider = OllamaProvider(base_url="http://127.0.0.1:1", timeout=0.01)
    registry = ModelRegistry()
    registry.register_provider(provider)
    assert registry.list_models() == []
