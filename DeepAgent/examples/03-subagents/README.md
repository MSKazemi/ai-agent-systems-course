# Example 03 — Subagents

An orchestrator agent that delegates subtasks to isolated child agents.

## What It Shows

- How the `task` tool creates a child agent with a fresh context
- How an orchestrator collects results from multiple subagents
- The difference in context usage between one big agent and subagents

## Run It

```bash
cd DeepAgent
source .venv/bin/activate
python examples/03-subagents/agent.py
```

## The Pattern

```
Orchestrator Agent
    │
    ├── task("Analyze this dataset and return statistics")
    │       └── Child Agent 1 (fresh context)
    │
    ├── task("Write a Python function to process the data")
    │       └── Child Agent 2 (fresh context)
    │
    └── Combines results and returns final answer
```

## What to Watch For

- The orchestrator calls `task(...)` twice, not doing the work itself
- Each child agent runs with a fresh, empty context
- The orchestrator's context stays small (it only sees the final results)
- This is the key pattern for scaling agents to large tasks
