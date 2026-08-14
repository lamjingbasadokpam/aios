"""Unified registry record joining identity and execution profile."""

from __future__ import annotations

from dataclasses import dataclass

from .identity import AgentIdentity
from .profile import AgentExecutionProfile


@dataclass(frozen=True, slots=True)
class AgentRecord:
    identity: AgentIdentity
    profile: AgentExecutionProfile

    def __post_init__(self) -> None:
        if str(self.identity.agent_id) != self.profile.agent_id:
            raise ValueError("identity.agent_id and profile.agent_id must match")

    @property
    def agent_id(self):
        return self.identity.agent_id

    def as_dict(self) -> dict:
        return {"identity": self.identity, "profile": self.profile.as_dict()}
