# 04 – FastMCP Explained

# 🧩 What Is MCP?

**MCP (Model Context Protocol)** is a standard.

It defines:

* How a client and server talk
* How tools are described
* How resources are accessed
* How prompts are structured
* How capabilities are negotiated

It is **a protocol**, not a library.

Think:

> MCP = HTTP for LLM tool calling

---

# 🧠 What Is the MCP SDK?

The **MCP SDK** is the official reference implementation of MCP.

GitHub: [https://github.com/modelcontextprotocol](https://github.com/modelcontextprotocol)

It is:

* Lower-level
* More protocol-focused
* More explicit
* Closer to the spec

It is what defines the standard behavior.

---

# 🚀 What Is FastMCP?

**FastMCP** is a Python framework that helps you build MCP servers (and clients) easily.

It is:

* High-level
* Developer-friendly
* Opinionated
* Focused on productivity

Website: [https://gofastmcp.com](https://gofastmcp.com)

### What FastMCP Does

It:

* Implements the MCP protocol for you
* Lets you register tools with decorators
* Handles transport (stdio / HTTP)
* Manages JSON-RPC messaging
* Handles schema generation automatically

Example:

```python
from fastmcp import FastMCP

mcp = FastMCP()

@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b

mcp.run()
```

That’s it. FastMCP handles the rest.

---


# 🔍 Key Difference

| Feature            | FastMCP                      | MCP SDK                          |
| ------------------ | ---------------------------- | -------------------------------- |
| Purpose            | Developer-friendly framework | Official protocol implementation |
| Abstraction level  | High                         | Low                              |
| Ease of use        | Very easy                    | More manual                      |
| Production-ready   | Yes                          | Yes                              |
| Good for teaching  | Excellent                    | More technical                   |
| Closer to MCP spec | Not directly                 | Yes                              |

---

# 🏗 Think of It Like This

If MCP is like:

> HTTP

Then:

* MCP SDK = low-level HTTP library
* FastMCP = FastAPI for MCP

FastMCP builds on MCP concepts and simplifies usage.

---

# 🧠 When Should You Use What?

## Use FastMCP if:

* You want to build an MCP server quickly
* You are teaching
* You want clean decorators
* You want minimal boilerplate
* You want both server and client easily

## Use MCP SDK if:

* You want full control
* You are implementing custom transport
* You are contributing to the protocol
* You want to follow the spec exactly
* You are building infrastructure-level tools

---

# ⚡ Final Summary

* MCP = protocol (standard)
* MCP SDK = official implementation of the protocol
* FastMCP = developer-friendly framework built to simplify MCP usage


# 🔍 What FastMCP Hides
FastMCP lets you focus on tools and logic while it handles the protocol.

---

## What FastMCP Hides

| Concern               | What you'd do manually | What FastMCP does |
|-----------------------|------------------------|-------------------|
| JSON-RPC              | Serialize/parse messages | Built-in |
| Schema generation     | Write tool schemas by hand | From Python type hints |
| Transport             | Implement stdio/HTTP   | `mcp.run()` handles it |
| Session management   | Track state, lifecycle | Handled for you |

---

## From Function to Tool

You write:

```python
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b
```

FastMCP automatically:
- Infers the JSON schema from `a: int`, `b: int`
- Uses the docstring as the tool description
- Registers the tool with the MCP server
- Handles validation and error responses

---

## The Abstraction Trade-off

| Pro                          | Con                          |
|------------------------------|------------------------------|
| Less boilerplate             | Less control over low-level details |
| Fast iteration               | May need to drop down for edge cases |
| Pythonic, readable           | Tied to FastMCP's conventions |

For learning and most projects, the pros outweigh the cons.

---

## When You Might Go Deeper

- Custom transports
- Special session handling
- Integrating with non-Python systems
- Debugging protocol-level issues

The MCP spec is open; you can implement servers in any language.

**Next:** [05 – IDE Setup](05-ide-setup.md) – Add MCP to VS Code/Cursor and use in Chat. Then try the [exercises](../exercises/).
