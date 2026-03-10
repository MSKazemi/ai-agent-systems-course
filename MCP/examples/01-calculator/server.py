"""
Minimal MCP server – two tools, nothing else.

Simple explanations:
- FastMCP: the server object. Clients connect to it and call tools.
- @mcp.tool(): a decorator. It registers the function below as a tool that clients can call.
  Without it, the function would be a normal Python function, not an MCP tool.
- mcp.run(): start the server and wait for clients. The process stays running until you stop it.
"""
from fastmcp import FastMCP

mcp = FastMCP("Calculator")


@mcp.tool()  # register add as a tool clients can call
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


@mcp.tool()  # register subtract as a tool clients can call
def subtract(a: int, b: int) -> int:
    """Subtract b from a."""
    return a - b


if __name__ == "__main__":
    # start the server
    mcp.run()
