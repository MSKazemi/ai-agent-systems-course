# Example 01 — Hello Agent

The simplest possible DeepAgent. One file, one goal, one result.

## What It Shows

- How to create an agent with `create_deep_agent()`
- How to send a message and get a response
- How the built-in tools appear in the output

## Run It

```bash
cd DeepAgent
source .venv/bin/activate
python examples/01-hello-agent/agent.py
```

## What to Watch For

The agent will automatically:
1. Call `write_todos` to break the task into steps
2. Call `read_file` / `ls` to read context if needed
3. Return a final answer

You don't write any of that logic — DeepAgent provides it.

## Expected Output

```
Agent response:
=== Step 1: Planning ===
[write_todos called with: ["Step 1: ...", "Step 2: ..."]]

=== Final Answer ===
Here is a summary of what I found: ...
```
