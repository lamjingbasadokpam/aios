"""CLI entry point for AIOS Kernel V0."""

from __future__ import annotations

import argparse
import asyncio

from aios.kernel import Agent, Kernel, Task
from aios.model import ModelRegistry, ModelRouter
from aios.model.mock import MockLocalProvider
from aios.recovery import RetryRecoveryHandler
from aios.runtime import AgentRuntime
from aios.tools import ToolGateway, ToolRegistry


def build_runtime() -> AgentRuntime:
    models = ModelRegistry()
    models.register_provider(MockLocalProvider())
    return AgentRuntime(
        ModelRouter(models),
        ToolGateway(ToolRegistry()),
        recovery_handler=RetryRecoveryHandler(1),
    )


def build_kernel() -> Kernel:
    return Kernel(agent_runtime=build_runtime())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="aios", description="AIOS local-first Agent OS")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("start", help="Start the kernel")
    sub.add_parser("status", help="Show kernel status")
    sub.add_parser("agent-list", help="List registered agents")

    agent = sub.add_parser("agent-create", help="Register an agent")
    agent.add_argument("name")

    task = sub.add_parser("task-create", help="Create and execute a task")
    task.add_argument("input")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    # V0 is intentionally process-local. Persistent daemon state comes later.
    kernel = build_kernel()
    kernel.start()

    if args.command == "start":
        print("AIOS Kernel V0 started.")
    elif args.command == "status":
        print(f"AIOS Kernel V0: {'running' if kernel.started else 'stopped'}")
    elif args.command == "agent-list":
        print(f"Agents: {len(kernel.agents)}")
    elif args.command == "agent-create":
        agent = kernel.register_agent(Agent(name=args.name))
        print(f"Agent created: {agent.name} ({agent.agent_id})")
    elif args.command == "task-create":
        task = kernel.create_task(Task(input=args.input))
        task = asyncio.run(kernel.run_task_async(task.task_id))
        if task.status.value == "failed":
            print(f"Task failed: {task.result}")
            return 1
        print(f"Task completed: {task.result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
