"""In-memory registries for the Kernel V0."""

from __future__ import annotations

from typing import Generic, TypeVar
from uuid import UUID

T = TypeVar("T")


class Registry(Generic[T]):
    """Small typed registry used by the initial local kernel."""

    def __init__(self) -> None:
        self._items: dict[UUID, T] = {}

    def add(self, item: T, item_id: UUID) -> T:
        if item_id in self._items:
            raise ValueError(f"Resource already registered: {item_id}")
        self._items[item_id] = item
        return item

    def get(self, item_id: UUID) -> T | None:
        return self._items.get(item_id)

    def remove(self, item_id: UUID) -> T | None:
        return self._items.pop(item_id, None)

    def list(self) -> list[T]:
        return list(self._items.values())

    def __len__(self) -> int:
        return len(self._items)
