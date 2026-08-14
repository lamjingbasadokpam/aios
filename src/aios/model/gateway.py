"""Provider-neutral model runtime gateway."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass(frozen=True, slots=True)
class ModelRequest:
    model: str
    messages: tuple[dict[str, Any], ...]
    parameters: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ModelResponse:
    model: str
    content: str
    finish_reason: str | None = None
    usage: dict[str, int] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


class ModelAdapter(Protocol):
    async def generate(self, request: ModelRequest) -> ModelResponse: ...


class ModelGateway:
    """Routes model requests to an explicitly registered provider adapter."""

    def __init__(self) -> None:
        self._adapters: dict[str, ModelAdapter] = {}

    def register(self, provider: str, adapter: ModelAdapter) -> None:
        if not provider.strip():
            raise ValueError("provider is required")
        if provider in self._adapters:
            raise ValueError(f"Model provider already registered: {provider}")
        self._adapters[provider] = adapter

    async def generate(self, provider: str, request: ModelRequest) -> ModelResponse:
        try:
            adapter = self._adapters[provider]
        except KeyError as exc:
            raise LookupError(f"No model provider registered: {provider}") from exc
        return await adapter.generate(request)
