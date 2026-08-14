"""Helpers for discovering local model providers."""

from __future__ import annotations

from .contracts import Model
from .registry import ModelRegistry


def discover_local_models(registry: ModelRegistry, providers: list[object]) -> list[Model]:
    """Register available local providers and return discovered models.

    Providers that are unavailable simply contribute no models. This keeps
    startup resilient when an optional local runtime is not running.
    """
    discovered: list[Model] = []
    for provider in providers:
        register = getattr(registry, "register_provider")
        register(provider)
        discovered.extend(provider.list_models())
    return discovered
