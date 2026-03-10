"""
SQLite Tool client – FastMCP Client, STDIO transport.

Same patterns: async with to connect, await to call tools. STDIO = client spawns server.
"""
import asyncio
from pathlib import Path

from fastmcp import Client

EXAMPLE_DIR = Path(__file__).resolve().parent
client = Client(str(EXAMPLE_DIR / "server.py"))


async def main():
    async with client:  # connect, run, disconnect
        tools = await client.list_tools()
        print(f"Tools: {[t.name for t in tools]}")

        result = await client.call_tool(
            "sql_query",
            {"query": "SELECT * FROM tasks"},
        )
        print(f"sql_query(SELECT * FROM tasks) =>\n{result.data}")


if __name__ == "__main__":
    asyncio.run(main())
