# Exercise 01 – Build a Tool

## Goal

Add a new tool to the Calculator example and explore type handling.

## Tasks

1. **Add `multiply(a: int, b: int)`** to `examples/01-calculator/server.py`.
   - Give it a clear docstring.
   - Return the product of `a` and `b`.

2. **Run the server** and test `multiply` via your MCP client.

3. **Experiment:** What happens if you pass non-integer values (e.g., `2.5` or `"hello"`)?
   - Observe the behavior. Does FastMCP validate types? What error do you see?

## Hints

- Copy the pattern from `add` and `subtract`.
- If you're unsure about type validation, try it and document what you see.

## Solution

See [../solutions/solution-01/](../solutions/solution-01/) when you're done.
