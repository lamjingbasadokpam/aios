"""Deterministic local mock provider used for contract tests and development."""

from __future__ import annotations

import json

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
            text=json.dumps({"action": "final", "answer": answer}),
            model_id=model.model_id,
            provider=self.provider_id,
            request_id=request.request_id,
            finish_reason="stop",
        )

    async def stream(self, request: InferenceRequest, model: Model):
        answer = f"[mock-local] {self._task_from_prompt(request.prompt)}"
        text = json.dumps({"action": "final", "answer": answer})
        for token in text.split():
            yield token + " "
