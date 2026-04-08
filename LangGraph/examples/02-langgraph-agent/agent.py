"""
Example 02 — LangGraph: Minimal ReAct Agent

Shows the ReAct loop as an explicit LangGraph graph:
  agent node → (tool calls?) → tool node → agent node → … → END

This is the same structure that DeepAgent uses internally.

Run:
  python LangGraph/examples/02-langgraph-agent/agent.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from dotenv import load_dotenv, find_dotenv
from typing import Annotated
from typing_extensions import TypedDict

from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

load_dotenv(find_dotenv())

from llm_config import get_langchain_model  # noqa: E402


# ── Tools ────────────────────────────────────────────────────

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b


@tool
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


tools = [multiply, add]


# ── State ─────────────────────────────────────────────────────

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


# ── Nodes ─────────────────────────────────────────────────────

model = get_langchain_model()
model_with_tools = model.bind_tools(tools)


def call_model(state: AgentState):
    """Ask the LLM what to do next."""
    response = model_with_tools.invoke(state["messages"])
    return {"messages": [response]}


# ── Graph ─────────────────────────────────────────────────────

def should_continue(state: AgentState):
    """Route: if the last message has tool calls, run them; else we're done."""
    last = state["messages"][-1]
    if last.tool_calls:
        return "tools"
    return END


builder = StateGraph(AgentState)
builder.add_node("agent", call_model)
builder.add_node("tools", ToolNode(tools))

builder.set_entry_point("agent")
builder.add_conditional_edges("agent", should_continue)
builder.add_edge("tools", "agent")   # after tools, always back to agent

graph = builder.compile()


# ── Run ───────────────────────────────────────────────────────

def run(question: str):
    print(f"Question: {question}")
    print("-" * 50)

    result = graph.invoke({
        "messages": [HumanMessage(content=question)]
    })

    # Walk through the message history to show what happened
    for msg in result["messages"]:
        role = type(msg).__name__
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for tc in msg.tool_calls:
                print(f"  [{role}] → tool call: {tc['name']}({tc['args']})")
        elif hasattr(msg, "content") and msg.content:
            print(f"  [{role}]: {msg.content}")

    print()


if __name__ == "__main__":
    run("What is 6 multiplied by 7?")
    run("What is (15 + 27) multiplied by 3?")
