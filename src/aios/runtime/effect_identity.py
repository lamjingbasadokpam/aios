"""Canonical effect identity and idempotency-key generation for AIOS."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class EffectIntent:
    """Logical identity of an external side effect."""

    run_id: str
    workflow_step: str
    tool: str
    arguments: dict[str, Any]
    effect_version: str = "v1"

    def canonical(self) -> str:
        payload = {
            "run_id": self.run_id,
            "workflow_step": self.workflow_step,
            "tool": self.tool,
            "arguments": self.arguments,
            "effect_version": self.effect_version,
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

    def key(self) -> str:
        return hashlib.sha256(self.canonical().encode("utf-8")).hexdigest()
