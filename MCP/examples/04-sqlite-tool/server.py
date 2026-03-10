"""
SQLite Tool server – one tool to run read-only SQL queries.

Simple explanations:
- sqlite3: built-in Python module for SQLite databases.
- get_connection(): returns a database connection. We open, use, then close it.
- The if __name__ block below creates a sample DB with a tasks table if it doesn't exist.
"""
import sqlite3
from pathlib import Path

from fastmcp import FastMCP

DB_PATH = Path(__file__).parent / "database.db"
mcp = FastMCP("SQLite Tool")


def get_connection():
    """Get a connection to the SQLite database."""
    return sqlite3.connect(DB_PATH)


@mcp.tool()
def sql_query(query: str) -> str:  # only SELECT allowed; no INSERT/UPDATE/DELETE
    """Execute a read-only SQL query on the sample database. Use SELECT only."""
    if ";" in query and "SELECT" not in query.upper().split(";")[0]:
        return "Error: Only SELECT queries are allowed."
    if "INSERT" in query.upper() or "UPDATE" in query.upper() or "DELETE" in query.upper():
        return "Error: Write operations are not allowed."
    try:
        conn = get_connection()  # open connection
        cur = conn.execute(query)
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description] if cur.description else []
        conn.close()  # always close connection when done
        if not cols:
            return f"Query executed. Rows affected: {len(rows)}"
        return "\n".join([str(dict(zip(cols, row))) for row in rows])
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    # create sample database if it doesn't exist
    if not DB_PATH.exists():
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            "CREATE TABLE tasks (id INTEGER PRIMARY KEY, title TEXT, done INTEGER)"
        )
        conn.execute("INSERT INTO tasks (title, done) VALUES ('Learn MCP', 1)")
        conn.execute("INSERT INTO tasks (title, done) VALUES ('Build a tool', 0)")
        conn.commit()
        conn.close()
    mcp.run()
