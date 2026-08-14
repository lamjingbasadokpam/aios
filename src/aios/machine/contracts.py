"""Explicit capability and policy contracts for machine access."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class Capability(StrEnum):
    FILE_READ = "file.read"
    FILE_WRITE = "file.write"
    PROCESS_EXEC = "process.exec"
    NETWORK = "network"
    ENV_READ = "env.read"


class Decision(StrEnum):
    ALLOW = "allow"
    DENY = "deny"
    APPROVAL_REQUIRED = "approval_required"


@dataclass(frozen=True, slots=True)
class CapabilityRequest:
    capability: Capability
    resource: str
    actor: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Policy:
    allowed: frozenset[Capability] = frozenset()
    approval_required: frozenset[Capability] = frozenset()

    def decide(self, request: CapabilityRequest) -> Decision:
        if request.capability in self.approval_required:
            return Decision.APPROVAL_REQUIRED
        if request.capability in self.allowed:
            return Decision.ALLOW
        return Decision.DENY
