"""Registry for unified AIOS agent records."""

from __future__ import annotations

from uuid import UUID

from .identity import AgentIdentity
from .record import AgentRecord


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: dict[UUID, AgentIdentity] = {}
        self._records: dict[UUID, AgentRecord] = {}

    def register(self, identity: AgentIdentity) -> AgentIdentity:
        if identity.agent_id in self._agents:
            raise ValueError(f"Agent already registered: {identity.agent_id}")
        self._agents[identity.agent_id] = identity
        return identity

    def register_record(self, record: AgentRecord) -> AgentRecord:
        if record.agent_id in self._records:
            raise ValueError(f"Agent record already registered: {record.agent_id}")
        self._records[record.agent_id] = record
        self._agents[record.agent_id] = record.identity
        return record

    def get(self, agent_id: UUID) -> AgentIdentity | None:
        return self._agents.get(agent_id)

    def get_record(self, agent_id: UUID) -> AgentRecord | None:
        return self._records.get(agent_id)

    def list(self, *, enabled_only: bool = False) -> tuple[AgentIdentity, ...]:
        agents = self._agents.values()
        if enabled_only:
            agents = (agent for agent in agents if agent.enabled)
        return tuple(agents)

    def list_records(self, *, enabled_only: bool = False) -> tuple[AgentRecord, ...]:
        records = self._records.values()
        if enabled_only:
            records = (record for record in records if record.identity.enabled)
        return tuple(records)

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
        if agent_id in self._records:
            record = self._records[agent_id]
            self._records[agent_id] = AgentRecord(updated, record.profile)
        return updated

    def remove(self, agent_id: UUID) -> AgentIdentity:
        self._records.pop(agent_id, None)
        return self._agents.pop(agent_id)
