# Exercise 02 – Add a Resource

## Goal

Expose a resource (read-only data) alongside tools.

## Tasks

1. **Create a new example** `examples/04-hello-resource/` with a FastMCP server.

2. **Add a resource** that returns a static string (e.g., "Hello from MCP!") when fetched.
   - Use FastMCP's resource API (check the FastMCP docs for `@mcp.resource()` or equivalent).
   - Assign it a URI like `hello://greeting`.

3. **Run the server** and verify a client can fetch the resource.

4. **Document** in a README: what URI to use and what content is returned.

## Hints

- Resources are typically registered with a URI template.
- The model fetches them when it needs contextual data.

## Solution

See [../solutions/solution-02/](../solutions/solution-02/) when you're done.
