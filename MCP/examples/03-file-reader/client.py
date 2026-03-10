"""
File Reader client – FastMCP Client, STDIO transport.

Same patterns as other clients: async with to connect, await to call tools.
Client spawns server as subprocess and talks over stdin/stdout.
"""
import asyncio
from pathlib import Path

from fastmcp import Client

EXAMPLE_DIR = Path(__file__).resolve().parent
client = Client(str(EXAMPLE_DIR / "server.py"))  # STDIO: pass server path


async def main():
    async with client:  # connect, then disconnect when done
        tools = await client.list_tools()
        print(f"Tools: {[t.name for t in tools]}")

        result = await client.call_tool(
            "read_file",
            {"path": str(EXAMPLE_DIR / "README.md")},
        )
        print(f"read_file(README.md) =>\n{result.data[:200]}...")


if __name__ == "__main__":
    asyncio.run(main())
