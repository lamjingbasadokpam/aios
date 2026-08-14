import asyncio
from datetime import datetime, timedelta, timezone

from aios.scheduler import ScheduledTask, Scheduler, TaskPriority


def test_scheduler_runs_due_task() -> None:
    seen = []

    async def handler(ctx):
        seen.append(ctx["x"])

    async def scenario():
        scheduler = Scheduler(max_concurrency=2)
        scheduler.schedule(ScheduledTask("due", handler, priority=TaskPriority.HIGH))
        count = await scheduler.run_once({"x": 7})
        assert count == 1
        assert seen == [7]

    asyncio.run(scenario())


def test_scheduler_respects_future_run_time() -> None:
    async def handler(ctx):
        raise AssertionError("must not run")

    async def scenario():
        scheduler = Scheduler()
        scheduler.schedule(ScheduledTask("future", handler, run_at=datetime.now(timezone.utc) + timedelta(hours=1)))
        assert await scheduler.run_once() == 0

    asyncio.run(scenario())


def test_scheduler_supports_bounded_recurring_runs() -> None:
    seen = []

    async def handler(ctx):
        seen.append(1)

    async def scenario():
        scheduler = Scheduler()
        scheduler.schedule(ScheduledTask("repeat", handler, interval_seconds=0, max_runs=2))
        await scheduler.run_once()
        await scheduler.run_once()
        await scheduler.run_once()
        assert len(seen) == 2

    asyncio.run(scenario())
