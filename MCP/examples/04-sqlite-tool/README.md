# Example 04 – SQLite Tool

MCP server and client for querying SQLite.

## Structure

| File | Role |
|------|------|
| `server.py` | FastMCP server – exposes `sql_query` (SELECT only) |
| `client.py` | MCP client – runs `SELECT * FROM tasks` |

## How to Run

From repo root (with venv activated):

```bash
# Server only (creates database.db on first run)
python examples/04-sqlite-tool/server.py

# Client – connects and queries tasks
python examples/04-sqlite-tool/client.py
```

## What to Observe

1. Client calls `sql_query` with `SELECT * FROM tasks`.
2. Server returns rows from the sample `tasks` table.

## Schema

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    title TEXT,
    done INTEGER
);
```

Sample rows: "Learn MCP" (done=1), "Build a tool" (done=0).

## Security Note

This example restricts to SELECT only. In production, add further guards (allowed tables, query timeouts, etc.).
