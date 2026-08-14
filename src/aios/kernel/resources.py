"""Resource primitives and registry for Kernel V0."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(slots=True)
class Resource:
    type: str
    capacity: float = 1.0
    available: float = 1.0
    resource_id: UUID = field(default_factory=uuid4)
    capabilities: set[str] = field(default_factory=set)
    locality: str = "local"
    health: str = "healthy"


class ResourceRegistry:
    def __init__(self) -> None:
        self._resources: dict[UUID, Resource] = {}

    def register(self, resource: Resource) -> Resource:
        if resource.resource_id in self._resources:
            raise ValueError(f"Resource already registered: {resource.resource_id}")
        self._resources[resource.resource_id] = resource
        return resource

    def get(self, resource_id: UUID) -> Resource | None:
        return self._resources.get(resource_id)

    def list(self) -> list[Resource]:
        return list(self._resources.values())
