# Solution 03 – Multi-Tool Server

## Design

- In-memory dict `notes: dict[str, str]` for storage.
- Four tools: `create_note`, `list_notes`, `get_note`, `delete_note`.
- Clear error messages when a note is not found.

## Usage

1. Run `python server.py`
2. Create: `create_note("Shopping", "Milk, eggs")`
3. List: `list_notes()` → "- Shopping"
4. Get: `get_note("Shopping")` → "Milk, eggs"
5. Delete: `delete_note("Shopping")` → "Note 'Shopping' deleted."
