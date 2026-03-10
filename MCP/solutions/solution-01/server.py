"""Solution for calculator exercise – add, subtract, multiply. Same patterns as 01-calculator."""
from fastmcp import FastMCP

mcp = FastMCP("Calculator")


@mcp.tool()  # register as MCP tool
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract b from a."""
    return a - b


@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b


if __name__ == "__main__":
    mcp.run()  # start the server
