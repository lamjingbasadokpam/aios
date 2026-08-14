"""Conservative local machine runtime; privileged operations remain adapters."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Callable

from .contracts import Capability, CapabilityRequest, Decision, Policy


class LocalMachineRuntime:
    def __init__(self, policy: Policy | None = None) -> None:
        self.policy = policy or Policy()
        self._approval_handler: Callable[[CapabilityRequest], bool] | None = None

    def set_approval_handler(self, handler: Callable[[CapabilityRequest], bool]) -> None:
        self._approval_handler = handler

    def authorize(self, request: CapabilityRequest) -> Decision:
        decision = self.policy.decide(request)
        if decision == Decision.APPROVAL_REQUIRED and self._approval_handler:
            return Decision.ALLOW if self._approval_handler(request) else Decision.DENY
        return decision

    def read_text(self, path: str, actor: str) -> str:
        request = CapabilityRequest(Capability.FILE_READ, str(Path(path).resolve()), actor)
        if self.authorize(request) != Decision.ALLOW:
            raise PermissionError(f"Denied: {request.capability} {request.resource}")
        return Path(path).read_text(encoding="utf-8")

    def read_env(self, name: str, actor: str) -> str | None:
        request = CapabilityRequest(Capability.ENV_READ, name, actor)
        if self.authorize(request) != Decision.ALLOW:
            raise PermissionError(f"Denied: {request.capability} {request.resource}")
        return os.environ.get(name)
