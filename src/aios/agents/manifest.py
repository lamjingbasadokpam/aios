"""Declarative agent manifest loading and validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from .profile import AgentExecutionProfile
from aios.runtime.resources import ResourceLimits


class ManifestError(ValueError):
    pass


class AgentManifestLoader:
    """Loads YAML manifests with strict root validation."""

    def load_text(self, text: str) -> AgentExecutionProfile:
        try:
            import yaml
        except ImportError as exc:
            raise ManifestError("PyYAML is required to load agent manifests") from exc
        try:
            raw = yaml.safe_load(text)
        except yaml.YAMLError as exc:
            raise ManifestError(f"invalid YAML manifest: {exc}") from exc
        if not isinstance(raw, Mapping):
            raise ManifestError("manifest root must be a mapping")
        return self.from_mapping(raw)

    def load_file(self, path: str | Path) -> AgentExecutionProfile:
        return self.load_text(Path(path).read_text(encoding="utf-8"))

    def from_mapping(self, raw: Mapping[str, Any]) -> AgentExecutionProfile:
        if not isinstance(raw, Mapping):
            raise ManifestError("manifest root must be a mapping")
        model = raw.get("model")
        if isinstance(model, Mapping):
            model = f"{model.get('provider', 'unknown')}/{model.get('name', '')}"
        resources = raw.get("resources") or {}
        if not isinstance(resources, Mapping):
            raise ManifestError("resources must be a mapping")
        transport = raw.get("transport") or {}
        if not isinstance(transport, Mapping):
            raise ManifestError("transport must be a mapping")
        return AgentExecutionProfile(
            agent_id=str(raw.get("id", "")),
            model=str(model or ""),
            sandbox_profile=str(raw.get("sandbox", "")),
            resources=ResourceLimits(
                max_processes=resources.get("processes"),
                memory_bytes=resources.get("memory_bytes"),
                cpu_time_seconds=resources.get("cpu_time_seconds"),
            ),
            network_allowed=bool(raw.get("network", False)),
            tools=tuple(str(x) for x in (raw.get("tools") or [])),
            transport=str(transport.get("type", "in_process")),
            environment={str(k): str(v) for k, v in (raw.get("environment") or {}).items()},
            metadata=dict(raw.get("metadata") or {}),
        )
