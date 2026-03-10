# Example 02 – Calculator Advanced

Same domain as 01, but with more FastMCP features.

## What's New (vs 01-calculator)

| Feature | 01 (Minimal) | 02 (Advanced) |
|---------|--------------|---------------|
| Transport | In-memory (same process) | STDIO (subprocess) |
| Tools | add, subtract | add, subtract, multiply, divide |
| Resource | — | `calc://info` |
| Prompt | — | `compute_expression` |
| Server instructions | — | Yes |

## Structure

| File | Role |
|------|------|
| `server.py` | FastMCP server – tools, resource, prompt |
| `client.py` | FastMCP Client – STDIO, lists all, calls tools |

## Run

From repo root (venv active):

```bash
# Server (optional – client spawns it)
python examples/02-calculator-advanced/server.py

# Client – connects via STDIO, demos all features
python examples/02-calculator-advanced/client.py
```

## References

- [FastMCP Server](https://gofastmcp.com/servers/server)
- [FastMCP Client](https://gofastmcp.com/clients/client)
