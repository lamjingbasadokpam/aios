"""Runtime startup rehydration for effect recovery state."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .effect_recovery_events import EffectRecoveryEvent
from .recovery_replay import RecoveryEventReplayer, ReplayedEffectState


@dataclass(frozen=True, slots=True)
class RecoveryState:
    effects: dict[str, ReplayedEffectState]


class RecoveryStateRehydrator:
    """Rebuilds the effect recovery projection before runtime execution resumes."""

    def __init__(self, replayer: RecoveryEventReplayer | None = None) -> None:
        self.replayer = replayer or RecoveryEventReplayer()

    def rehydrate(self, events: Iterable[EffectRecoveryEvent]) -> RecoveryState:
        return RecoveryState(self.replayer.replay(events))

    def is_safe_to_resume(self, state: RecoveryState) -> bool:
        return not any(
            effect.state == "reconciliation_required" for effect in state.effects.values()
        )
