"""Deterministic local mock provider used for contract tests and development."""

from __future__ import annotations

from aios.model.contracts import InferenceRequest, InferenceResponse, Model, ModelCapabilities


class MockLocalProvider:
    provider_id = "mock-local"

    def list_models(self) -> list[Model]:
        return [
            Model(
                model_id="mock-local/default",
                provider=self.provider_id,
                capabilities=ModelCapabilities(streaming=True, structured_output=True),
                locality="local",
                context_limit=8192,
                health="healthy",
            )
        ]

    async def generate(self, request: InferenceRequest, model: Model) -> InferenceResponse:
        return InferenceResponse(
            text=f"[mock-local] {request.prompt}",
            model_id=model.model_id,
            provider=self.provider_id,
            request_id=request.request_id,
            finish_reason="stop",
        )

    async def stream(self, request: InferenceRequest, model: Model):
        text = f"[mock-local] {request.prompt}"
        for token in text.split():
            yield token + " "
