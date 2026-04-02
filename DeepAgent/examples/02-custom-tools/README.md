# Example 02 — Custom Tools

Add your own Python functions as tools that the agent can call.

## What It Shows

- How to define a custom tool with `@tool`
- How to register it with `create_deep_agent(tools=[...])`
- How the agent decides when to call your tool vs built-in tools

## Run It

```bash
cd DeepAgent
source .venv/bin/activate
python examples/02-custom-tools/agent.py
```

## Key Code Pattern

```python
from langchain_core.tools import tool
from deepagents import create_deep_agent

@tool
def get_stock_price(ticker: str) -> str:
    """Get the current stock price for a ticker symbol."""
    # Your real logic here
    return f"{ticker}: $150.00"

agent = create_deep_agent(
    model=llm,
    tools=[get_stock_price],   # <-- add your tools here
)
```

## What to Watch For

- The LLM reads the tool's docstring to understand when to call it
- Your tool appears alongside the built-in tools in the agent's tool list
- The agent calls your tool when the task requires it
