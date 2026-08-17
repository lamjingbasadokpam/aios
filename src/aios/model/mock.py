"""Deterministic in-process model provider for the AIOS CLI and tests."""

from __future__ import annotations

from .contracts import InferenceRequest, InferenceResponse, Model, ModelCapabilities


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

    @staticmethod
    def _task_from_prompt(prompt: str) -> str:
        marker = "TASK:\n"
        if marker not in prompt:
            return prompt
        task = prompt.split(marker, 1)[1]
        return task.split("\n\nHISTORY:", 1)[0]

    async def generate(self, request: InferenceRequest, model: Model) -> InferenceResponse:
        answer = f"[mock-local] {self._task_from_prompt(request.prompt)}"
        return InferenceResponse(
            text=answer,
            model_id=model.model_id,
            provider=self.provider_id,
            request_id=request.request_id,
            finish_reason="stop",
            metadata={"action": "final"},
        )

    async def stream(self, request: InferenceRequest, model: Model):
        answer = f"[mock-local] {self._task_from_prompt(request.prompt)}"
        for token in answer.split():
            yield token + " "
