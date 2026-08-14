"""Ollama HTTP adapter for AIOS Model Fabric.

Uses only Python's standard library so the core project does not depend on an
Ollama SDK. Ollama itself remains an optional local runtime.
"""

from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from aios.model.contracts import (
    InferenceRequest,
    InferenceResponse,
    Model,
    ModelCapabilities,
)


class OllamaConnectionError(RuntimeError):
    """Raised when the local Ollama service cannot be reached."""


class OllamaProvider:
    provider_id = "ollama"

    def __init__(self, base_url: str = "http://127.0.0.1:11434", timeout: float = 30.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _request_json(self, path: str, payload: dict | None = None) -> dict:
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        request = Request(
            f"{self.base_url}{path}",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST" if payload is not None else "GET",
        )
        try:
            with urlopen(request, timeout=self.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except (URLError, TimeoutError, HTTPError) as exc:
            raise OllamaConnectionError(f"Ollama request failed: {exc}") from exc

    def health(self) -> bool:
        try:
            self._request_json("/api/tags")
            return True
        except OllamaConnectionError:
            return False

    def list_models(self) -> list[Model]:
        try:
            payload = self._request_json("/api/tags")
        except OllamaConnectionError:
            return []

        models: list[Model] = []
        for item in payload.get("models", []):
            name = item.get("name")
            if not name:
                continue
            models.append(
                Model(
                    model_id=name,
                    provider=self.provider_id,
                    capabilities=ModelCapabilities(
                        streaming=True,
                        tool_calling=True,
                        structured_output=True,
                    ),
                    locality="local",
                    health="healthy",
                    resource_requirements={"runtime": "ollama"},
                )
            )
        return models

    async def generate(self, request: InferenceRequest, model: Model) -> InferenceResponse:
        prompt = request.prompt
        if request.system_prompt:
            prompt = f"{request.system_prompt}\n\n{prompt}"

        payload = {
            "model": model.model_id,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": request.temperature,
            },
        }
        if request.max_tokens is not None:
            payload["options"]["num_predict"] = request.max_tokens

        result = self._request_json("/api/generate", payload)
        return InferenceResponse(
            text=result.get("response", ""),
            model_id=model.model_id,
            provider=self.provider_id,
            request_id=request.request_id,
            finish_reason="stop" if result.get("done") else None,
            usage={
                "prompt_eval_count": result.get("prompt_eval_count"),
                "eval_count": result.get("eval_count"),
            },
        )

    async def stream(self, request: InferenceRequest, model: Model):
        # Streaming is intentionally deferred until the async transport layer is
        # introduced. Keeping the provider contract here prevents that decision
        # from leaking into the rest of AIOS.
        raise NotImplementedError("Ollama streaming adapter is planned for V1")
