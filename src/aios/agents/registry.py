"""In-process reference registry for durable agent identities."""

from __future__ import annotations

from uuid import UUID

from .identity import AgentIdentity


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: dict[UUID, AgentIdentity] = {}

    def register(self, identity: AgentIdentity) -> AgentIdentity:
        if identity.agent_id in self._agents:
            raise ValueError(f"Agent already registered: {identity.agent_id}")
        self._agents[identity.agent_id] = identity
        return identity

    def get(self, agent_id: UUID) -> AgentIdentity | None:
        return self._agents.get(agent_id)

    def list(self, *, enabled_only: bool = False) -> tuple[AgentIdentity, ...]:
        agents = self._agents.values()
        if enabled_only:
            agents = (agent for agent in agents if agent.enabled)
        return tuple(agents)

    def enable(self, agent_id: UUID) -> AgentIdentity:
        return self._replace(agent_id, enabled=True)

    def disable(self, agent_id: UUID) -> AgentIdentity:
        return self._replace(agent_id, enabled=False)

    def _replace(self, agent_id: UUID, **changes: object) -> AgentIdentity:
        current = self._agents.get(agent_id)
        if current is None:
            raise KeyError(agent_id)
        updated = AgentIdentity(
            name=changes.get("name", current.name),
            role=changes.get("role", current.role),
            model=changes.get("model", current.model),
            memory_namespace=changes.get("memory_namespace", current.memory_namespace),
            sandbox_profile=changes.get("sandbox_profile", current.sandbox_profile),
            tools=changes.get("tools", current.tools),
            metadata=changes.get("metadata", current.metadata),
            agent_id=current.agent_id,
            enabled=changes.get("enabled", current.enabled),
        )
        self._agents[agent_id] = updated
        return updated
