"""Stable model-fabric contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, AsyncIterator, Protocol
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class ModelCapabilities:
    text_generation: bool = True
    streaming: bool = False
    embeddings: bool = False
    vision: bool = False
    tool_calling: bool = False
    structured_output: bool = False
    reasoning: bool = False


@dataclass(frozen=True, slots=True)
class Model:
    model_id: str
    provider: str
    capabilities: ModelCapabilities
    locality: str = "local"
    context_limit: int | None = None
    resource_requirements: dict[str, Any] = field(default_factory=dict)
    health: str = "unknown"


@dataclass(frozen=True, slots=True)
class InferenceRequest:
    prompt: str
    model_id: str | None = None
    system_prompt: str | None = None
    temperature: float = 0.2
    max_tokens: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    request_id: UUID = field(default_factory=uuid4)


@dataclass(frozen=True, slots=True)
class InferenceResponse:
    text: str
    model_id: str
    provider: str
    request_id: UUID
    usage: dict[str, Any] = field(default_factory=dict)
    finish_reason: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class ModelProvider(Protocol):
    """Provider adapter contract. Concrete providers live outside the kernel."""

    @property
    def provider_id(self) -> str: ...

    def list_models(self) -> list[Model]: ...

    async def generate(self, request: InferenceRequest, model: Model) -> InferenceResponse: ...

    async def stream(self, request: InferenceRequest, model: Model) -> AsyncIterator[str]: ...
