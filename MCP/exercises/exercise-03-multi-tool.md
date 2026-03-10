# Exercise 03 – Multi-Tool Server

## Goal

Build a small MCP server with multiple related tools.

## Tasks

1. **Design** a "Notes" server with at least:
   - `create_note(title: str, content: str)` – stores a note in memory
   - `list_notes()` – returns all note titles
   - `get_note(title: str)` – returns the content of a note by title

2. **Implement** it in `examples/05-notes-server/` (create the folder).

3. **Use in-memory storage** (e.g., a dict) – no database required.

4. **Test** with your MCP client: create a note, list notes, get a note.

5. **Optional:** Add `delete_note(title: str)` and handle "note not found" errors.

## Hints

- Keep state in a module-level variable.
- Return clear error messages for missing notes.

## Solution

See [../solutions/solution-03/](../solutions/solution-03/) when you're done.
