from aios.runtime.budget import BudgetDecision, BudgetPolicy, ResourceBudget, ResourceUsage


def test_budget_allows_usage_within_limits() -> None:
    policy = BudgetPolicy(ResourceBudget(max_tokens=100, max_tool_calls=5, max_cost=1.0))
    result = policy.evaluate(ResourceUsage(tokens=80, tool_calls=2, cost=0.4))
    assert result.decision == BudgetDecision.ALLOW


def test_budget_denies_when_any_limit_is_exceeded() -> None:
    policy = BudgetPolicy(ResourceBudget(max_tokens=100, max_tool_calls=5))
    result = policy.evaluate(ResourceUsage(tokens=101, tool_calls=1))
    assert result.decision == BudgetDecision.DENY
    assert "token budget" in result.reason
