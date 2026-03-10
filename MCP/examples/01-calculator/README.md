# Example 01 – Calculator (Minimal)

Smallest MCP example: FastMCP server + FastMCP Client. In-memory (same process).

## Structure

| File | Role |
|------|------|
| `server.py` | FastMCP server – 2 tools |
| `client.py` | FastMCP Client – in-memory |
| `demo.py` | Fake LLM loop – `add 4 and 5` → result |

## How to Run

From repo root (venv active):

```bash
python examples/01-calculator/server.py   # Server standalone
python examples/01-calculator/client.py   # Client (in-memory) → add(3,7)=10
python examples/01-calculator/demo.py     # Interactive fake LLM
```

## What to Observe

- **client.py** uses `Client(mcp)` – same process, no subprocess
- **demo.py** parses "add 4 and 5" → tool call → result

## Next

[02-calculator-advanced](../02-calculator-advanced/) – same domain, more features (STDIO, resources, prompts).
