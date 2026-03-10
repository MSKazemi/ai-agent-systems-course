"""
Notes Server – create, list, get, delete notes. In-memory storage (dict).

Simple explanations:
- notes: a dict that holds title → content. Lives in memory; lost when server stops.
"""
from fastmcp import FastMCP

mcp = FastMCP("Notes Server")
notes: dict[str, str] = {}  # in-memory storage


@mcp.tool()
def create_note(title: str, content: str) -> str:  # store in notes dict
    """Create a new note with the given title and content."""
    notes[title] = content
    return f"Note '{title}' created."


@mcp.tool()
def list_notes() -> str:
    """List all note titles."""
    if not notes:
        return "No notes yet."
    return "\n".join(f"- {t}" for t in notes.keys())


@mcp.tool()
def get_note(title: str) -> str:
    """Get the content of a note by title."""
    if title not in notes:
        return f"Error: Note '{title}' not found."
    return notes[title]


@mcp.tool()
def delete_note(title: str) -> str:
    """Delete a note by title."""
    if title not in notes:
        return f"Error: Note '{title}' not found."
    del notes[title]
    return f"Note '{title}' deleted."


if __name__ == "__main__":
    mcp.run()
