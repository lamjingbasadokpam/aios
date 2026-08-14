"""Lifecycle-to-event translation for the AIOS runtime."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from .events import RuntimeEvent
from .lifecycle import LifecycleState, RuntimeRun


@dataclass(slots=True)
class LifecycleEventEmitter:
    """Builds canonical runtime events for lifecycle transitions."""

    source: str = "runtime.lifecycle"

    def emit(self, run: RuntimeRun, event_type: str, payload: dict[str, Any] | None = None) -> RuntimeEvent:
        return RuntimeEvent(
            event_id=str(uuid4()),
            type=event_type,
            timestamp=datetime.now(timezone.utc),
            source=self.source,
            run_id=run.run.run_id,
            payload={"state": run.state.value, **(payload or {})},
        )

    def transition(self, run: RuntimeRun, state: LifecycleState) -> RuntimeEvent:
        run.state = state
        return self.emit(run, f"run.{state.value}")
