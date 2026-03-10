# Example 03 – File Reader

MCP server and client for reading files.

## Structure

| File | Role |
|------|------|
| `server.py` | FastMCP server – exposes `read_file` |
| `client.py` | MCP client – calls `read_file` on README.md |

## How to Run

From repo root (with venv activated):

```bash
# Server only
python examples/03-file-reader/server.py

# Client – connects and reads README.md
python examples/03-file-reader/client.py
```

## What to Observe

1. Client calls `read_file` with path to README.md.
2. Server returns file contents (or error if not found).

## Security Note

This example reads from the filesystem. In production, restrict paths (e.g., allowlist directories) to avoid exposing sensitive files.

## Next

[04-sqlite-tool](../04-sqlite-tool/) – database integration.
