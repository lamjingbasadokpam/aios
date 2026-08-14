"""CLI entry point for AIOS Kernel V0."""

from __future__ import annotations

import argparse

from aios.kernel import Agent, Kernel, Task


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="aios", description="AIOS local-first Agent OS")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("start", help="Start the kernel")
    sub.add_parser("status", help="Show kernel status")
    sub.add_parser("agent-list", help="List registered agents")

    agent = sub.add_parser("agent-create", help="Register an agent")
    agent.add_argument("name")

    task = sub.add_parser("task-create", help="Create and accept a task")
    task.add_argument("input")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    # V0 is intentionally process-local. Persistent daemon state comes later.
    kernel = Kernel()
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
        print(f"Task created: {task.task_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
