"""
Full demo: User → Real LLM → FastMCP Client → Server → Result.

Simple explanations:
- llm_config: selects LLM provider (Ollama / Azure / Gemini) from env vars.
  Set LLM_PROVIDER=ollama (default), LLM_PROVIDER=azure, or LLM_PROVIDER=gemini.
- mcp_tools_to_openai: converts MCP tool schemas → OpenAI tool-calling format so the
  LLM knows what tools are available and what arguments they expect.
- tool_choice="auto": the LLM decides whether to call a tool or answer directly.
- asyncio.run(): run an async function from sync code.
"""
import asyncio
import json
import sys
from pathlib import Path

from dotenv import load_dotenv
from fastmcp import Client
from server import mcp

# Add MCP root to path so we can import llm_config
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

load_dotenv()

from llm_config import get_openai_client  # noqa: E402

llm_client, llm_model = get_openai_client()


def mcp_tools_to_openai(tools: list) -> list:
    """Convert MCP tool list → OpenAI tool-calling format."""
    return [
        {
            "type": "function",
            "function": {
                "name": t.name,
                "description": t.description or "",
                "parameters": t.inputSchema or {"type": "object", "properties": {}},
            },
        }
        for t in tools
    ]


async def _list_tools():
    async with Client(mcp) as c:
        return await c.list_tools()


async def _call_tool(tool_name: str, arguments: dict):
    async with Client(mcp) as c:
        result = await c.call_tool(tool_name, arguments)
        return result.data


def llm_pick_tool(user_input: str, openai_tools: list):
    """Send user message + available tools to the LLM; return (tool_name, args) or (None, None)."""
    response = llm_client.chat.completions.create(
        model=llm_model,
        messages=[{"role": "user", "content": user_input}],
        tools=openai_tools,
        tool_choice="auto",
    )
    msg = response.choices[0].message
    if msg.tool_calls:
        tc = msg.tool_calls[0]
        return tc.function.name, json.loads(tc.function.arguments)
    return None, None


def main():
    print("Full MCP demo (Real LLM + FastMCP Client + Server)")
    print(f"Provider: {llm_model}")
    print("Try: 'add 4 and 5'  |  'what is 10 minus 3?'  |  'quit'")
    print("-" * 50)

    tools = asyncio.run(_list_tools())
    openai_tools = mcp_tools_to_openai(tools)

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not user_input or user_input.lower() in ("quit", "exit", "q"):
            print("Bye!")
            break

        tool_name, arguments = llm_pick_tool(user_input, openai_tools)
        if tool_name is None:
            print("(LLM didn't select a tool — try rephrasing as a math question)")
            continue

        print(f"  [LLM]    → {tool_name}({arguments})")
        result = asyncio.run(_call_tool(tool_name, arguments))
        print(f"  [Server] → {result}")


if __name__ == "__main__":
    main()
