import pytest

from aios.runtime.policy import AllowListPolicy, Decision, PolicyRequest


@pytest.mark.asyncio
async def test_allow_list_policy_allows_explicit_action() -> None:
    policy = AllowListPolicy({"filesystem": {"read"}})
    result = await policy.evaluate(PolicyRequest("run-1", "filesystem", "read"))
    assert result.decision == Decision.ALLOW


@pytest.mark.asyncio
async def test_allow_list_policy_denies_unknown_action() -> None:
    policy = AllowListPolicy({"filesystem": {"read"}})
    result = await policy.evaluate(PolicyRequest("run-1", "filesystem", "write"))
    assert result.decision == Decision.DENY
