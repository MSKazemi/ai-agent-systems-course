# Solution 01 – Build a Tool

## What Was Added

- `multiply(a: int, b: int)` – returns the product of two integers.

## Type Validation

FastMCP validates tool arguments against the declared schema. If you pass non-integers (e.g., `2.5` or `"hello"`), the client or server will typically return a validation error before the tool runs. The exact message depends on the client implementation.
