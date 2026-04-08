"""
Example 01 — LangChain: Chat Model + Tool Calling

Shows:
  1. Create a chat model via llm_config
  2. Define a tool with @tool
  3. Bind the tool to the model
  4. Invoke and handle a tool call manually

Run:
  python LangGraph/examples/01-chain-and-tools/example.py
"""

import sys
from pathlib import Path

# Add repo root to path so we can import llm_config
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from dotenv import load_dotenv, find_dotenv
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage

load_dotenv(find_dotenv())

from llm_config import get_langchain_model  # noqa: E402


# ── Step 1: Define a tool ────────────────────────────────────

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers and return the result."""
    return a * b


@tool
def add(a: int, b: int) -> int:
    """Add two integers and return the result."""
    return a + b


tools = [multiply, add]
tool_map = {t.name: t for t in tools}


# ── Step 2: Bind tools to the model ─────────────────────────

model = get_langchain_model()
model_with_tools = model.bind_tools(tools)


# ── Step 3: Invoke ───────────────────────────────────────────

def run(question: str):
    print(f"Question: {question}")
    print("-" * 50)

    messages = [HumanMessage(content=question)]

    # First call — model may respond with tool calls
    response = model_with_tools.invoke(messages)
    messages.append(response)

    # If the model called a tool, execute it and feed back the result
    if response.tool_calls:
        for tc in response.tool_calls:
            print(f"  Tool call: {tc['name']}({tc['args']})")
            result = tool_map[tc["name"]].invoke(tc["args"])
            print(f"  Tool result: {result}")
            messages.append(
                ToolMessage(content=str(result), tool_call_id=tc["id"])
            )

        # Second call — model now has the tool result
        final = model_with_tools.invoke(messages)
        print(f"\nAnswer: {final.content}")
    else:
        print(f"\nAnswer: {response.content}")


if __name__ == "__main__":
    run("What is 6 multiplied by 7?")
    print()
    run("Add 15 and 27, then tell me the result.")
