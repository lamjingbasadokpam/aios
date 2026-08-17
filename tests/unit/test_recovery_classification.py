import asyncio
from types import SimpleNamespace

from aios.recovery import RetryRecoveryHandler
from aios.recovery.classification import RecoveryClass, classify_failure
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
        return SimpleNamespace(success=True, output="ok", error=None, tool_id=tool_id)


def test_failure_classes_are_explicit():
    assert classify_failure(TimeoutError()) is RecoveryClass.TRANSIENT
    assert classify_failure(ConnectionError()) is RecoveryClass.TRANSIENT
    assert classify_failure(PermissionError()) is RecoveryClass.POLICY
    assert classify_failure(ValueError("bad input")) is RecoveryClass.TERMINAL


def test_terminal_model_failure_does_not_retry():
    async def scenario():
        router = FakeRouter([ValueError("bad model output")])
        runtime = AgentRuntime(router, FakeGateway(), recovery_handler=RetryRecoveryHandler(3))
        return await runtime.run("hello"), router

    result, router = asyncio.run(scenario())
    assert result.success is False
    assert router.calls == 1


def test_policy_failure_does_not_retry():
    async def scenario():
        router = FakeRouter([PermissionError("denied")])
        runtime = AgentRuntime(router, FakeGateway(), recovery_handler=RetryRecoveryHandler(3))
        return await runtime.run("hello"), router

    result, router = asyncio.run(scenario())
    assert result.success is False
    assert result.error == "denied"
    assert router.calls == 1


def test_transient_model_failure_can_retry():
    async def scenario():
        router = FakeRouter([TimeoutError("temporary"), '{"action":"final","answer":"ok"}'])
        runtime = AgentRuntime(router, FakeGateway(), recovery_handler=RetryRecoveryHandler(1))
        return await runtime.run("hello"), router

    result, router = asyncio.run(scenario())
    assert result.success is True
    assert result.output == "ok"
    assert router.calls == 2
