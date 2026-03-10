"""
Advanced Calculator – tools, resource, prompt, instructions.

Simple explanations:
- instructions: hint for the AI on how to use this server (shown in some clients).
- @mcp.resource("uri"): expose read-only data at a URI. Clients can list and read it.
- @mcp.prompt(): expose a prompt template. Clients can list and use it.
"""
from fastmcp import FastMCP

mcp = FastMCP(
    name="Calculator Advanced",
    instructions="Use these tools for basic math. Call compute for expressions.",
)


@mcp.tool()
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


@mcp.tool()
def divide(a: int, b: int) -> float:
    """Divide a by b. Returns float."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


@mcp.resource("calc://info")  # expose data at this URI; clients read it
def calculator_info() -> str:
    """Info about this calculator."""
    return "Calculator Advanced v1.0 – add, subtract, multiply, divide"


@mcp.prompt()  # expose a prompt template clients can use
def compute_expression(expression: str) -> str:
    """Create a prompt to compute a math expression."""
    return f"Compute the following: {expression}"


if __name__ == "__main__":
    mcp.run()
