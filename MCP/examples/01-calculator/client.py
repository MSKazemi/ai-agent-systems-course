"""
Minimal MCP client – FastMCP Client, in-memory (same process).

Simple explanations:
- async: a function that can wait without blocking. Use it when you call await inside.
- await: wait for this to finish before moving to the next line.
  (If there were other async tasks, they could run while this one waits.)
- async with: when we ENTER the block, the client connects (starts talking to the server).
  When we EXIT the block, it disconnects (stops and cleans up). Connect = ready to talk;
  disconnect = done, close the connection.
"""
import asyncio
from fastmcp import Client
from server import mcp

client = Client(mcp)


async def main():
    """main is async because we use await inside."""
    # async with client: connect when we enter, disconnect when we leave
    async with client:
        # await: wait for this to finish before moving on
        tools = await client.list_tools()
        print(f"Tools: {[t.name for t in tools]}")

        result = await client.call_tool("add", {"a": 3, "b": 7})
        print(f"add(3, 7) => {result.data}")


if __name__ == "__main__":
    # run the async function main()
    asyncio.run(main())
