"""Route recovery alerts to independent operational sinks."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

from .recovery_alerts import RecoveryAlert


@dataclass(frozen=True, slots=True)
class RecoveryAlertRoute:
    code: str
    sink: str


class RecoveryAlertRouter:
    """Dispatches alerts by code without coupling detection to delivery."""

    def __init__(self, routes: Iterable[RecoveryAlertRoute], sinks: dict[str, Callable[[RecoveryAlert], None]]) -> None:
        self._routes = list(routes)
        self._sinks = sinks

    def route(self, alert: RecoveryAlert) -> list[str]:
        delivered: list[str] = []
        for route in self._routes:
            if route.code != "*" and route.code != alert.code:
                continue
            sink = self._sinks.get(route.sink)
            if sink is None:
                continue
            sink(alert)
            delivered.append(route.sink)
        return delivered
