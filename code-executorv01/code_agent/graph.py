"""
LangGraph ReAct agent graph.

Three nodes wired into a loop:

  agent  →  tools  →  finalize  →  END
    ↑          |
    └──────────┘  (on failure, loop back to agent)

The agent node calls the LLM — it MUST produce a tool call.
The tools node runs execute_python.
The finalize node calls the LLM one last time to write the plain-text answer.
"""

import sys
from enum import Enum
from typing import TypedDict, Annotated, Optional

from langchain_core.messages import AIMessage, ToolMessage, SystemMessage
from langgraph.graph import StateGraph, add_messages
from langgraph.prebuilt import ToolNode

from llm_wrapper import OllamaEnforcingWrapper
from config import MAX_ITERATIONS, OLLAMA_HOST, OLLAMA_MODEL


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

class ExtendedState(TypedDict):
    """
    Flows through every graph node.

    - messages: the full conversation (managed by add_messages — appends, never replaces)
    - data_context: description of the loaded dataset, injected into the system prompt
    - attempts: counts only agent-node LLM calls (not tool runs, not finalize)
    - finalize_retries: how many times finalize has been retried (max 1)
    """
    messages: Annotated[list, add_messages]
    data_context: str
    attempts: int
    finalize_retries: int


# ---------------------------------------------------------------------------
# Routing targets
# ---------------------------------------------------------------------------

class Route(str, Enum):
    TOOLS = "tools"
    FINALIZE = "finalize"
    AGENT = "agent"
    END = "__end__"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _latest_tool_message(state: ExtendedState) -> Optional[ToolMessage]:
    for m in reversed(state["messages"]):
        if isinstance(m, ToolMessage):
            return m
    return None


def _tool_failed(msg: Optional[ToolMessage]) -> bool:
    return bool(msg) and "[PYTHON_EXECUTION_FAILED]" in (msg.content or "").upper()


def _tool_succeeded(msg: Optional[ToolMessage]) -> bool:
    if not msg:
        return False
    up = (msg.content or "").upper()
    return "SUCCESS" in up and "[PYTHON_EXECUTION_FAILED]" not in up


def _is_protocol_error(msg: object) -> bool:
    if not isinstance(msg, AIMessage):
        return False
    md = getattr(msg, "metadata", None) or {}
    return isinstance(md, dict) and md.get("parse_status") in {"PROTOCOL_ERROR", "PARSE_ERROR"}


def _last_success_output(messages: list) -> Optional[str]:
    for m in reversed(messages):
        if isinstance(m, ToolMessage) and _tool_succeeded(m):
            return (m.content or "").strip() or None
    return None


# ---------------------------------------------------------------------------
# Nodes
# ---------------------------------------------------------------------------

def agent_node(state: ExtendedState, llm_wrapper: OllamaEnforcingWrapper) -> dict:
    """Call the LLM — must produce a tool call."""
    attempts = state.get("attempts", 0) + 1
    print(f"[AGENT] attempt {attempts}/{MAX_ITERATIONS}", file=sys.stderr)

    response = llm_wrapper.invoke(state["messages"], allow_text=False)
    return {"messages": [response], "attempts": attempts}


def finalize_node(state: ExtendedState, llm_wrapper: OllamaEnforcingWrapper) -> dict:
    """
    One final LLM call to turn raw tool output into a clean answer.
    Retried at most once if the LLM produces a tool call here (forbidden).
    Falls back to a deterministic summary if retries are exhausted.
    """
    retries = state.get("finalize_retries", 0)

    if retries > 1:
        # Give up on the LLM and emit a deterministic answer
        output = _last_success_output(state.get("messages") or [])
        content = f"Task completed.\n\n{output}" if output else "Task completed."
        msg = AIMessage(content=content)
        msg.metadata = {"parse_status": "FALLBACK", "allow_text": True}
        return {"messages": [msg], "finalize_retries": retries}

    response = llm_wrapper.invoke(state["messages"], allow_text=True)

    if _is_protocol_error(response):
        return {"messages": [response], "finalize_retries": retries + 1}

    return {"messages": [response], "finalize_retries": retries}


# ---------------------------------------------------------------------------
# Routing
# ---------------------------------------------------------------------------

def route_from_agent(state: ExtendedState) -> Route:
    last = state["messages"][-1]
    attempts = state.get("attempts", 0)
    tool_calls = getattr(last, "tool_calls", []) or []
    latest_tool = _latest_tool_message(state)

    if attempts >= MAX_ITERATIONS:
        print(f"[ROUTE] Max iterations reached.", file=sys.stderr)
        return Route.END

    if _is_protocol_error(last):
        print("[ROUTE] Protocol error → retry agent", file=sys.stderr)
        return Route.AGENT

    if tool_calls:
        print(f"[ROUTE] Tool call → tools", file=sys.stderr)
        return Route.TOOLS

    # No tool call but there's an unresolved error — ask the LLM to fix it
    if _tool_failed(latest_tool):
        print("[ROUTE] Exec error, no tool call → retry agent", file=sys.stderr)
        return Route.AGENT

    print("[ROUTE] No tool call → retry agent", file=sys.stderr)
    return Route.AGENT


def route_from_tools(state: ExtendedState) -> Route:
    latest_tool = _latest_tool_message(state)
    attempts = state.get("attempts", 0)

    if attempts >= MAX_ITERATIONS:
        return Route.END

    if _tool_failed(latest_tool):
        print("[ROUTE] Tool failed → back to agent", file=sys.stderr)
        return Route.AGENT

    if _tool_succeeded(latest_tool):
        print("[ROUTE] Tool succeeded → finalize", file=sys.stderr)
        return Route.FINALIZE

    return Route.AGENT


def route_from_finalize(state: ExtendedState) -> Route:
    last = state["messages"][-1]
    retries = state.get("finalize_retries", 0)

    if _is_protocol_error(last) or (getattr(last, "tool_calls", None)):
        if retries <= 1:
            return Route.FINALIZE
        return Route.FINALIZE  # triggers fallback path inside finalize_node

    return Route.END


# ---------------------------------------------------------------------------
# Graph builder
# ---------------------------------------------------------------------------

def create_graph(tools: list, system_prompt: str):
    print(f"[GRAPH] Building graph | {OLLAMA_MODEL} @ {OLLAMA_HOST}", file=sys.stderr)

    llm_wrapper = OllamaEnforcingWrapper(tools=tools)

    def _agent(state: ExtendedState) -> dict:
        messages = state.get("messages") or []
        if not any(isinstance(m, SystemMessage) for m in messages):
            state = {**state, "messages": [SystemMessage(content=system_prompt)] + messages}
        return agent_node(state, llm_wrapper)

    def _finalize(state: ExtendedState) -> dict:
        if "finalize_retries" not in state:
            state = {**state, "finalize_retries": 0}
        messages = state.get("messages") or []
        if not any(isinstance(m, SystemMessage) for m in messages):
            state = {**state, "messages": [SystemMessage(content=system_prompt)] + messages}
        return finalize_node(state, llm_wrapper)

    def _tools(state: ExtendedState) -> dict:
        return ToolNode(tools).invoke(state)

    workflow = StateGraph(ExtendedState)
    workflow.add_node("agent", _agent)
    workflow.add_node("tools", _tools)
    workflow.add_node("finalize", _finalize)
    workflow.set_entry_point("agent")

    workflow.add_conditional_edges("agent", route_from_agent, {
        Route.TOOLS: "tools",
        Route.AGENT: "agent",
        Route.END: "__end__",
    })
    workflow.add_conditional_edges("tools", route_from_tools, {
        Route.FINALIZE: "finalize",
        Route.AGENT: "agent",
        Route.END: "__end__",
    })
    workflow.add_conditional_edges("finalize", route_from_finalize, {
        Route.FINALIZE: "finalize",
        Route.END: "__end__",
    })

    graph = workflow.compile()
    print(f"[GRAPH] Ready (max {MAX_ITERATIONS} agent iterations)", file=sys.stderr)
    return graph
