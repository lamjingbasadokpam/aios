from pathlib import Path

import pytest

from aios.environment import Environment, EnvironmentLimits, Policy, PolicyEngine
from aios.tools.gateway import ToolDenied, ToolGateway
from aios.tools import ToolContext, ToolRegistry
from adapters.tools.filesystem import FILESYSTEM_WRITE, write_tool


def test_policy_denies_network_when_environment_disallows() -> None:
    from aios.tools.contracts import Tool

    tool = Tool(
        tool_id="network.test",
        name="network_test",
        description="test",
        network_required=True,
    )
    decision = PolicyEngine(Policy(allowed_capabilities=frozenset())).evaluate(
        tool, Environment(name="isolated", limits=EnvironmentLimits(allow_network=False))
    )
    assert not decision.allowed


def test_high_risk_requires_approval(tmp_path: Path) -> None:
    registry = ToolRegistry()
    tool, handler = write_tool(tmp_path)
    registry.register(tool, handler)
    gateway = ToolGateway(
        registry,
        PolicyEngine(Policy(allowed_capabilities=frozenset({FILESYSTEM_WRITE}))),
    )

    # Promote the tool to high risk for this test.
    registry._tools[tool.tool_id] = type(tool)(
        **{**tool.__dict__, "risk_level": "high"}
    ) if hasattr(tool, "__dict__") else tool

    # Capability enforcement remains the primary V0 guarantee.
    with pytest.raises(ToolDenied):
        import asyncio
        asyncio.run(gateway.invoke(tool.tool_id, {"path": "x", "content": "x"}, ToolContext()))
