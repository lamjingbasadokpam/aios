"""Capability-aware model router."""

from __future__ import annotations

from .contracts import InferenceRequest, InferenceResponse, Model
from .registry import ModelRegistry


class ModelRouter:
    def __init__(self, registry: ModelRegistry) -> None:
        self.registry = registry

    def select(self, request: InferenceRequest, *, locality: str | None = None,
               require: set[str] | None = None) -> tuple[Model, object]:
        required = require or set()
        candidates = self.registry.list_models()
        if request.model_id:
            candidates = [m for m in candidates if m.model_id == request.model_id]
        if locality:
            candidates = [m for m in candidates if m.locality == locality]

        for model in candidates:
            if model.health == "unavailable":
                continue
            if all(bool(getattr(model.capabilities, capability, False)) for capability in required):
                provider = self.registry.get_provider(model.provider)
                if provider is not None:
                    return model, provider
        raise LookupError("No compatible healthy model/provider found")

    async def generate(self, request: InferenceRequest, *, locality: str | None = None,
                       require: set[str] | None = None) -> InferenceResponse:
        model, provider = self.select(request, locality=locality, require=require)
        return await provider.generate(request, model)
