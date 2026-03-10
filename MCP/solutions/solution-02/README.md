# Solution 02 – Add a Resource

Resources in FastMCP are registered with `@mcp.resource()`. The implementation varies by FastMCP version – check the [FastMCP documentation](https://github.com/jlowin/fastmcp) for the current API.

Example pattern (verify against your FastMCP version):

```python
@mcp.resource("hello://greeting")
def get_greeting() -> str:
    return "Hello from MCP!"
```

The client fetches the resource by URI and receives the returned content.
