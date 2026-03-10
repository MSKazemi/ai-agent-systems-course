# FAQ – Model Context Protocol

Common questions and answers.

---

## Do I need Cursor or Claude Desktop?

No. Each example has a `client.py` using **FastMCP Client**:

- **01-calculator** – In-memory `Client(mcp)` – minimal
- **02-calculator-advanced** – STDIO `Client("server.py")` – more features
- **03-file-reader**, **04-sqlite-tool** – STDIO clients
- **01-calculator/demo.py** – Full loop with simulated LLM

For real LLM integration, use Cursor, Claude Desktop, or your own client + API.

## Does FastMCP support clients?

Yes. **FastMCP provides both server and client.** Use `fastmcp.Client` for the client side. See [gofastmcp.com/clients/client](https://gofastmcp.com/clients/client).

---

## Why not REST?

REST is great for humans and traditional apps. MCP is designed for **LLM ↔ tool** communication:

- **Structured for tool-calling:** Tools have names, typed params, descriptions – exactly what LLMs need
- **Bidirectional:** Supports streaming, multiple tools in one session
- **Standardized:** Same protocol across Cursor, Claude Desktop, custom clients
- **Schema-first:** Tool schemas are first-class; REST doesn't define this

You can still run an MCP server behind HTTP – transport is separate from the protocol.

---

## Why not LangChain?

LangChain offers agent frameworks and tool abstractions. MCP is a **protocol**:

- **LangChain:** Python library, specific to LangChain-based apps
- **MCP:** Protocol any client and server can implement, language-agnostic

You can use LangChain tools and expose them via MCP – they're complementary. MCP ensures your tools work with Cursor, Claude Desktop, and other MCP clients without LangChain.

---

## What is transport?

**Transport** is how the MCP client and server send messages:

| Transport | Use Case |
|-----------|----------|
| **stdio** | Local process, CLI tools |
| **HTTP/SSE** | Remote servers, web apps |

The protocol (JSON-RPC messages) is the same; only the carrier changes.

---

## Do I need to know JSON-RPC?

Not if you use FastMCP. It handles serialization, message routing, and session management. You focus on defining tools. If you implement a server from scratch (e.g., in another language), you'll need to follow the [MCP specification](https://spec.modelcontextprotocol.io/).

---

## How do I debug tool calls?

1. **Logging:** Add `print()` or `logging` in your tool functions
2. **Client logs:** Many MCP clients log requests and responses
3. **Schema:** Ensure your tool params match what the model sends (types, names)
4. **Test directly:** Some clients let you invoke tools manually for testing

---

## Is MCP secure?

MCP defines the protocol, not the security model. Security is your responsibility:

- Restrict tool capabilities (e.g., read-only DB, allowed paths)
- Run the server in a controlled environment
- Validate and sanitize all inputs
- Use transport-level security (HTTPS, auth) for remote servers
