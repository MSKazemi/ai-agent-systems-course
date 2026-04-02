"""
Example 01 — Hello Agent

The minimal DeepAgent:
  1. Load the LLM from environment config
  2. Create an agent with create_deep_agent()
  3. Send a message and print the response

No custom tools. No extra configuration.
The agent gets the full built-in toolkit automatically:
  write_todos, read_file, write_file, edit_file, ls, glob, grep, execute, task

Run:
  cd DeepAgent
  source .venv/bin/activate
  python examples/01-hello-agent/agent.py
"""

import sys
from pathlib import Path

# Add DeepAgent root to path so we can import llm_config
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from dotenv import load_dotenv
from deepagents import create_deep_agent
from llm_config import get_llm_model

load_dotenv()


def main():
    # Step 1: Load the LLM (configured via .env)
    llm = get_llm_model()

    # Step 2: Create the agent
    #   - model: the LLM to use
    #   - tools: [] means use only the built-in tools (write_todos, read_file, etc.)
    #   - system_prompt: optional; customizes the agent's persona
    agent = create_deep_agent(
        model=llm,
        system_prompt="You are a helpful assistant. Keep your answers concise.",
    )

    # Step 3: Define a task
    task = (
        "List the three most important things to know about the "
        "Model Context Protocol (MCP). Format as a numbered list."
    )

    print("Task:", task)
    print("-" * 60)

    # Step 4: Invoke the agent
    #   agent.invoke() runs the ReAct loop until the LLM stops calling tools
    result = agent.invoke({
        "messages": [{"role": "user", "content": task}]
    })

    # Step 5: Print the final response
    #   result["messages"] is the full message history
    #   The last message is the agent's final answer
    final_message = result["messages"][-1]
    print("\nAgent response:")
    print(final_message.content)


if __name__ == "__main__":
    main()
