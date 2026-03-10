"""File Reader server – one tool that reads files from disk."""
from pathlib import Path

from fastmcp import FastMCP

mcp = FastMCP("File Reader")


@mcp.tool()  # register as tool clients can call
def read_file(path: str) -> str:
    """Read the contents of a file. Provide a path relative to current directory or absolute."""
    p = Path(path)
    if not p.exists():
        return f"Error: File not found: {path}"
    if not p.is_file():
        return f"Error: Not a file: {path}"
    try:
        return p.read_text()
    except Exception as e:
        return f"Error reading file: {e}"


if __name__ == "__main__":
    mcp.run()  # start the server
