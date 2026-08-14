"""Severity-aware routing for recovery alerts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

from .recovery_alert_routing import RecoveryAlertRoute
from .recovery_alert_severity import ClassifiedRecoveryAlert, RecoveryAlertSeverity


@dataclass(frozen=True, slots=True)
class SeverityRecoveryAlertRoute:
    severity: RecoveryAlertSeverity
    sink: str


class SeverityAwareRecoveryAlertRouter:
    """Routes classified alerts using severity-specific and generic routes."""

    def __init__(self, routes: Iterable[SeverityRecoveryAlertRoute], sinks: dict[str, Callable[[ClassifiedRecoveryAlert], None]]) -> None:
        self._routes = list(routes)
        self._sinks = sinks

    def route(self, classified: ClassifiedRecoveryAlert) -> list[str]:
        delivered: list[str] = []
        for route in self._routes:
            if route.severity != classified.severity:
                continue
            sink = self._sinks.get(route.sink)
            if sink is None:
                continue
            sink(classified)
            delivered.append(route.sink)
        return delivered
