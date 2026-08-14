"""Declarative agent manifest loading and validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .profile import AgentExecutionProfile
from aios.runtime.resources import ResourceLimits


class ManifestError(ValueError):
    pass


class AgentManifestLoader:
    """Loads YAML manifests when PyYAML is installed, with strict validation."""

    def load_text(self, text: str) -> AgentExecutionProfile:
        try:
            import yaml
        except ImportError as exc:
            raise ManifestError("PyYAML is required to load agent manifests") from exc
        raw = yaml.safe_load(text)
        if not isinstance(raw, dict):
            raise ManifestError("manifest root must be a mapping")
        return self.from_mapping(raw)

    def load_file(self, path: str | Path) -> AgentExecutionProfile:
        return self.load_text(Path(path).read_text(encoding="utf-8"))

    def from_mapping(self, raw: dict[str, Any]) -> AgentExecutionProfile:
        model = raw.get("model")
        if isinstance(model, dict):
            model = f"{model.get('provider', 'unknown')}/{model.get('name', '')}"
        resources = raw.get("resources") or {}
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
            transport=str((raw.get("transport") or {}).get("type", "in_process")),
            environment={str(k): str(v) for k, v in (raw.get("environment") or {}).items()},
            metadata=dict(raw.get("metadata") or {}),
        )
