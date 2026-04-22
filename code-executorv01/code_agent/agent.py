"""
Entry point for the interactive CLI agent.

Loads data, builds the LangGraph graph, and runs the conversation loop.
"""

import sys
from typing import Optional, List

from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage

from config import MAX_ITERATIONS, MAX_MESSAGES, DEFAULT_DATA_FILE, TOOL_CALL_MODE
from tools import tools, load_data, _repl
from graph import create_graph
from system_prompt import get_system_prompt


# ---------------------------------------------------------------------------
# Data context
# ---------------------------------------------------------------------------

def format_data_context(metadata: dict) -> str:
    """
    Turn the metadata from load_data into a short description the LLM can read.
    This goes into the system prompt so the model knows the shape of 'df'.
    """
    ctx = ""

    if "data_preview" in metadata:
        ctx += f"**DATA PREVIEW:**\n```\n{metadata['data_preview']}\n```\n\n"

    ctx += (
        f"**LOADED DATA:** DataFrame 'df' "
        f"({metadata.get('rows', 0)} rows × {len(metadata.get('columns', []))} columns)"
    )
    if metadata.get("potential_time_index"):
        ctx += f" | Time index: '{metadata['potential_time_index']}'"
    ctx += "\n\n"

    if metadata.get("columns"):
        ctx += "**COLUMNS:** " + ", ".join(metadata["columns"]) + "\n\n"

    if metadata.get("numeric_columns"):
        ctx += "**NUMERIC COLUMNS (min, max, mean):**\n"
        for col, s in list(metadata["numeric_columns"].items())[:8]:
            ctx += f"- {col}: min={s['min']:.1f}, max={s['max']:.1f}, mean={s['mean']:.1f}\n"
        ctx += "\n"

    if metadata.get("datetime_columns"):
        ctx += "**DATETIME COLUMNS:**\n"
        for col, info in metadata["datetime_columns"].items():
            ctx += f"- {col}: {info.get('min')} → {info.get('max')} (duration: {info.get('duration')})\n"

    return ctx


# ---------------------------------------------------------------------------
# Conversation helpers
# ---------------------------------------------------------------------------

def _extract_final_answer(messages: List) -> Optional[str]:
    """Pick the last valid plain-text AIMessage (from finalize)."""
    for msg in reversed(messages):
        if not isinstance(msg, AIMessage):
            continue
        md = getattr(msg, "metadata", {}) or {}
        if md.get("allow_text") is not True:
            continue
        if md.get("parse_status") in {"PROTOCOL_ERROR", "PARSE_ERROR"}:
            continue
        content = (msg.content or "").strip()
        if not content:
            continue
        if getattr(msg, "tool_calls", None):
            continue
        return msg.content
    return None


def _extract_stdout(messages: List) -> Optional[str]:
    """Fallback: extract stdout from the last successful ToolMessage."""
    for msg in reversed(messages):
        if not isinstance(msg, ToolMessage):
            continue
        content = msg.content or ""
        if "SUCCESS" in content and "**STDOUT:**" in content:
            return content.split("**STDOUT:**", 1)[1].split("---")[0].strip()
    return None


def _prune(messages: list) -> list:
    """Keep the system prompt + the most recent MAX_MESSAGES messages."""
    if len(messages) <= MAX_MESSAGES:
        return messages
    return [messages[0]] + messages[-(MAX_MESSAGES - 1):]


# ---------------------------------------------------------------------------
# Single turn
# ---------------------------------------------------------------------------

def run_turn(query: str, graph, data_context: str, conversation: List) -> tuple[str, List]:
    """
    Run one user query through the graph.
    Returns (answer, updated_conversation).
    """
    user_msg = HumanMessage(content=f"**YOUR TASK:**\n{query}")
    input_messages = _prune(conversation + [user_msg])

    initial_state = {
        "messages": input_messages,
        "data_context": data_context,
        "attempts": 0,
        "finalize_retries": 0,
    }

    final_state = graph.invoke(initial_state)
    all_messages = final_state.get("messages", [])
    new_messages = all_messages[len(input_messages):]

    # Append new messages to conversation history
    conversation.extend(new_messages)

    answer = _extract_final_answer(new_messages)
    if not answer:
        stdout = _extract_stdout(new_messages)
        answer = f"Done.\n\n{stdout}" if stdout else "[Agent did not produce a final answer]"

    return answer, conversation


# ---------------------------------------------------------------------------
# Interactive loop
# ---------------------------------------------------------------------------

def interactive_loop(graph, data_context: str) -> None:
    print("\n" + "=" * 60)
    print("CODE EXECUTION AGENT")
    print(f"Model: {TOOL_CALL_MODE} mode | max {MAX_ITERATIONS} iterations per query")
    print("Commands: clear, quit")
    print("=" * 60)

    system_prompt = get_system_prompt()
    full_prompt = f"{system_prompt}\n\n{data_context}"
    conversation: List = [SystemMessage(content=full_prompt)]

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "q"):
            break

        if user_input.lower() == "clear":
            _repl.locals.clear()
            load_data(str(DEFAULT_DATA_FILE))
            conversation = [SystemMessage(content=full_prompt)]
            print("[CLEAR] Conversation and REPL reset.")
            continue

        answer, conversation = run_turn(user_input, graph, data_context, conversation)
        print(f"\nAgent:\n{answer}\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("\n" + "=" * 60)
    print("INITIALIZING")
    print("=" * 60)

    print(f"\n[1/2] Loading data: {DEFAULT_DATA_FILE}", file=sys.stderr)
    metadata = load_data(str(DEFAULT_DATA_FILE))
    if metadata is None:
        print("ERROR: Could not load data file.", file=sys.stderr)
        sys.exit(1)
    print(f" [OK] {metadata['rows']} rows × {len(metadata['columns'])} columns", file=sys.stderr)

    data_context = format_data_context(metadata)
    system_prompt = get_system_prompt()
    full_prompt = f"{system_prompt}\n\n{data_context}"

    print(f"\n[2/2] Building agent...", file=sys.stderr)
    try:
        graph = create_graph(tools, full_prompt)
        print(" [OK] Agent ready", file=sys.stderr)
    except Exception as e:
        print(f" [ERROR] {e}", file=sys.stderr)
        sys.exit(1)

    interactive_loop(graph, data_context)


if __name__ == "__main__":
    main()
