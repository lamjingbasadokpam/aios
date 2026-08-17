import asyncio
from types import SimpleNamespace

from aios.recovery import RetryRecoveryHandler
from aios.runtime import AgentRuntime


class FakeRouter:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.calls = 0

    async def generate(self, request, *, locality, require):
        self.calls += 1
        value = next(self.responses)
        if isinstance(value, Exception):
            raise value
        return SimpleNamespace(text=value)


class FakeGateway:
    async def invoke(self, tool_id, arguments, context):
        return SimpleNamespace(success=True, output="tool ok", error=None, tool_id=tool_id)


class FailingThenSuccessGateway:
    def __init__(self):
        self.calls = 0

    async def invoke(self, tool_id, arguments, context):
        self.calls += 1
        if self.calls == 1:
            return SimpleNamespace(success=False, output=None, error="temporary tool failure", tool_id=tool_id)
        return SimpleNamespace(success=True, output="tool recovered", error=None, tool_id=tool_id)


class PolicyFailingGateway:
    def __init__(self):
        self.calls = 0

    async def invoke(self, tool_id, arguments, context):
        self.calls += 1
        raise PermissionError("workspace boundary violation")


def test_model_failure_retries_then_succeeds():
    async def scenario():
        router = FakeRouter([RuntimeError("temporary"), '{"action":"final","answer":"ok"}'])
        runtime = AgentRuntime(router, FakeGateway(), recovery_handler=RetryRecoveryHandler(1))
        result = await runtime.run("hello")
        return result, router

    result, router = asyncio.run(scenario())
    assert result.success is True
    assert result.output == "ok"
    assert router.calls == 2


def test_tool_failure_retries_then_succeeds():
    async def scenario():
        router = FakeRouter([
            '{"action":"tool","tool_id":"echo","arguments":{}}',
            '{"action":"tool","tool_id":"echo","arguments":{}}',
            '{"action":"final","answer":"done"}',
        ])
        gateway = FailingThenSuccessGateway()
        runtime = AgentRuntime(router, gateway, recovery_handler=RetryRecoveryHandler(1))
        result = await runtime.run("use tool")
        return result, gateway

    result, gateway = asyncio.run(scenario())
    assert result.success is True
    assert result.output == "done"
    assert gateway.calls == 2


def test_policy_failure_does_not_retry():
    async def scenario():
        router = FakeRouter(['{"action":"tool","tool_id":"filesystem.read","arguments":{}}'])
        gateway = PolicyFailingGateway()
        runtime = AgentRuntime(router, gateway, recovery_handler=RetryRecoveryHandler(3))
        result = await runtime.run("read outside workspace")
        return result, gateway

    result, gateway = asyncio.run(scenario())
    assert result.success is False
    assert result.error == "workspace boundary violation"
    assert gateway.calls == 1
    assert len(result.tool_results) == 1


def test_recovery_exhaustion_returns_failure():
    async def scenario():
        router = FakeRouter([RuntimeError("still down"), RuntimeError("still down")])
        runtime = AgentRuntime(router, FakeGateway(), recovery_handler=RetryRecoveryHandler(1))
        result = await runtime.run("hello")
        return result, router

    result, router = asyncio.run(scenario())
    assert result.success is False
    assert result.error == "still down"
    assert router.calls == 2


def test_no_recovery_handler_preserves_immediate_failure():
    async def scenario():
        router = FakeRouter([RuntimeError("down")])
        runtime = AgentRuntime(router, FakeGateway())
        result = await runtime.run("hello")
        return result, router

    result, router = asyncio.run(scenario())
    assert result.success is False
    assert result.error == "down"
    assert router.calls == 1
