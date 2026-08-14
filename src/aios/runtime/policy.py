"""Provider-neutral runtime governance and authorization boundary."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Protocol


class Decision(str, Enum):
    ALLOW = "allow"
    DENY = "deny"


@dataclass(frozen=True, slots=True)
class PolicyRequest:
    run_id: str
    capability: str
    action: str
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    decision: Decision
    reason: str
    policy: str = "default"


class Policy(Protocol):
    async def evaluate(self, request: PolicyRequest) -> PolicyDecision: ...


class AllowListPolicy:
    """Simple explicit capability/action allow-list for the local runtime."""

    def __init__(self, rules: dict[str, set[str]]) -> None:
        self._rules = {capability: set(actions) for capability, actions in rules.items()}

    async def evaluate(self, request: PolicyRequest) -> PolicyDecision:
        allowed = request.action in self._rules.get(request.capability, set())
        if allowed:
            return PolicyDecision(Decision.ALLOW, "explicitly allowed", "allow-list")
        return PolicyDecision(Decision.DENY, "capability/action not allow-listed", "allow-list")
