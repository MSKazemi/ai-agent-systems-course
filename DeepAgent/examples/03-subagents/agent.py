"""
Example 03 — Subagents

Shows how DeepAgent spawns isolated child agents via the `task` tool.

The orchestrator agent is given a task too large to do in one context.
It automatically:
  1. Calls write_todos to plan
  2. Calls task(...) to delegate subtasks to child agents
  3. Each child runs in a fresh context with its own tool calls
  4. The orchestrator collects results and produces the final answer

This pattern is key for:
  - Avoiding context window overflow
  - Parallelizing independent subtasks
  - Keeping the orchestrator's context small

Run:
  cd DeepAgent
  source .venv/bin/activate
  python examples/03-subagents/agent.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from dotenv import load_dotenv
from deepagents import create_deep_agent
from llm_config import get_llm_model

load_dotenv()


def main():
    llm = get_llm_model()

    # The orchestrator has no custom tools.
    # It uses the built-in `task` tool to delegate to subagents.
    agent = create_deep_agent(
        model=llm,
        system_prompt=(
            "You are an orchestrator agent. When given a multi-part task, "
            "break it into subtasks and use the `task` tool to delegate each "
            "subtask to a specialized subagent. Combine their results at the end."
        ),
    )

    # This task has two independent subtasks that can be delegated separately:
    #   Subtask A: explain what a binary search tree is
    #   Subtask B: write a Python implementation of one
    #
    # The orchestrator should delegate each to a child agent,
    # then combine the results.
    task = (
        "I need two things:\n"
        "1. A clear explanation of what a binary search tree (BST) is, "
        "including its properties and time complexity.\n"
        "2. A Python class implementing a BST with insert, search, and "
        "in-order traversal methods, including docstrings.\n\n"
        "Please delegate each part to a separate subagent and combine the results."
    )

    print("Task:", task)
    print("-" * 60)
    print("Watch for: task(...) calls in the message history\n")

    result = agent.invoke({
        "messages": [{"role": "user", "content": task}]
    })

    # Show subagent calls made by the orchestrator
    print("--- Subagent delegations ---")
    for msg in result["messages"]:
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for tc in msg.tool_calls:
                if tc["name"] == "task":
                    # task tool receives the subtask description
                    description = tc["args"].get("description", tc["args"])
                    preview = str(description)[:80]
                    print(f"  task({preview!r}...)")

    print("\n--- Final Answer ---")
    final_message = result["messages"][-1]
    print(final_message.content)


if __name__ == "__main__":
    main()
