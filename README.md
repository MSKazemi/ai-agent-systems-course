# AI Agent Systems Course

A self-paced course on building AI agent systems with **MCP (Model Context Protocol)** and **A2A (Agent-to-Agent)**. Learn how LLMs connect to tools and how agents delegate to each other.

---

## Course Modules

| Module | What You'll Learn | Quick Start |
|--------|-------------------|-------------|
| **[MCP](MCP/)** | Tools, resources, prompts — LLMs calling external capabilities | `cd MCP && pip install -r requirements.txt && python examples/01-calculator/server.py` |
| **[A2A](A2A/)** | Agent orchestration — agents delegating to specialized sub-agents | `cd A2A && pip install -r requirements.txt` — see [A2A Quick Start](A2A/README.md#quick-start) |

---

## MCP — Model Context Protocol

**Goal:** Expose tools (calculators, file readers, databases) to LLMs via a standard protocol.

- Build MCP servers with **FastMCP**
- Understand tools vs resources vs prompts
- Connect to Cursor, VS Code, or Claude Desktop

**→ [MCP README](MCP/README.md)** — full learning path, examples, exercises

---

## A2A — Agent-to-Agent

**Goal:** Build agents that call other agents over HTTP. One coordinator delegates to specialized remote agents (math, prime checker, etc.).

- Use **Google ADK** with Azure OpenAI or Gemini
- Expose agents with `to_a2a()`, consume with `RemoteA2aAgent`
- Static vs dynamic orchestration (registry-based)

**→ [A2A README](A2A/README.md)** — architecture, quick start, teaching docs

---

## Project Structure

```
ai-agent-systems-course/
├── MCP/                    # Model Context Protocol — tools for LLMs
│   ├── docs/               # Teaching docs
│   ├── examples/           # Calculator, file reader, SQLite, etc.
│   ├── exercises/          # Hands-on tasks
│   └── solutions/          # Exercise answers
├── A2A/                    # Agent-to-Agent — agent orchestration
│   ├── docs/               # Teaching docs (9 sections)
│   ├── remote_math_agent.py
│   ├── remote_prime_agent.py
│   ├── coordinator_agent.py
│   └── dynamic_coordinator_agent.py
└── README.md
```

---

## Prerequisites

- **Python 3.10+**
- **MCP:** Basic Python (no prior MCP knowledge)
- **A2A:** API keys for Azure OpenAI or Google Gemini — see [A2A Environment Setup](A2A/docs/05-environment-setup.md)

---

## License

See [MCP/LICENSE](MCP/LICENSE) and A2A materials for licensing terms.
