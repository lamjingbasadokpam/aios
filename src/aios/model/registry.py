"""Model and provider registry."""

from __future__ import annotations

from .contracts import Model, ModelProvider


class ModelRegistry:
    def __init__(self) -> None:
        self._providers: dict[str, ModelProvider] = {}
        self._models: dict[str, Model] = {}

    def register_provider(self, provider: ModelProvider) -> None:
        self._providers[provider.provider_id] = provider
        for model in provider.list_models():
            self.register_model(model)

    def register_model(self, model: Model) -> None:
        self._models[model.model_id] = model

    def get_model(self, model_id: str) -> Model | None:
        return self._models.get(model_id)

    def get_provider(self, provider_id: str) -> ModelProvider | None:
        return self._providers.get(provider_id)

    def list_models(self) -> list[Model]:
        return list(self._models.values())
