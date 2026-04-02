# AI Agent Systems Course

A hands-on, self-paced course for building AI agent systems from the ground up.

---

## What Is an AI Agent?

A traditional program follows fixed instructions: input → logic → output.

An **AI agent** is different: it can *decide* what to do next. You give it a goal in natural language, and it figures out which tools to call, in what order, to accomplish that goal. It can call a calculator, search the web, query a database, or even hand off work to another agent — all without you writing explicit step-by-step code.

This course teaches three key technologies that make agents work in practice:

| Technology      | What it does                                                      | Analogy                             |
|-----------------|-------------------------------------------------------------------|-------------------------------------|
| **MCP**         | Gives an LLM access to external tools (calculators, files, DBs)   | A plugin system for AI              |
| **A2A**         | Lets one agent delegate tasks to other specialized agents         | A manager assigning work to experts |
| **DeepAgent**   | Gives a single agent planning, context management, and subagents  | A senior engineer with a task list  |

---

## Course Modules

### Recommended order: MCP → A2A → DeepAgent

Start with MCP — it introduces how LLMs call tools, which is the foundation for everything in A2A and DeepAgent.

| Module                                       | What You'll Build                                                       | Time       |
|----------------------------------------------|-------------------------------------------------------------------------|------------|
| **[MCP →](MCP/README.md)**                   | A server that exposes tools (calculator, file reader, database) to LLMs | ~2–3 hours |
| **[A2A →](A2A/README.md)**                   | Coordinator agent delegating math and prime checks to remote agents     | ~2–3 hours |
| **[DeepAgent →](DeepAgent/README.md)**       | A single agent that plans, manages context, and spawns subagents        | ~1–2 hours |

---

## Module 1 — MCP (Model Context Protocol)

**The idea:** An LLM on its own can only generate text. MCP is a standard protocol that lets an LLM say *"call this tool"*, and have that call actually execute on your machine or server.

You will build MCP servers and see exactly how a tool call flows from an LLM request to a Python function and back.

**What you'll learn:**

- How LLMs call external functions (tool calling)
- How to write MCP servers with FastMCP
- The difference between tools, resources, and prompts
- How to connect your server to VS Code, Cursor, or Claude Desktop

**[→ Start MCP module](MCP/README.md)**

---

## Module 2 — A2A (Agent-to-Agent)

**The idea:** As systems grow, one agent can't do everything well. A2A is a protocol for agents to call *other agents* over HTTP — each agent exposes a card describing its skills, and a coordinator routes requests to the right specialist.

You will run a coordinator agent that delegates arithmetic to a math agent and primality checks to a prime agent, each running as a separate process.

**What you'll learn:**

- How agents discover and communicate with each other
- How to expose an agent as an HTTP service
- How to build a coordinator that delegates to remote agents
- Static orchestration (hardcoded agents) vs dynamic orchestration (registry-based)

**[→ Start A2A module](A2A/README.md)**

---

## Module 3 — DeepAgent

**The idea:** A single agent has limits. When a task is large, the context window fills up; without a plan, steps get skipped; without subagents, everything runs sequentially. DeepAgent is a batteries-included harness that solves all three — built on LangChain and LangGraph.

You will build agents that plan multi-step tasks, read and write files to manage context, and delegate subtasks to isolated child agents.

**What you'll learn:**

- How an agent harness differs from a raw LLM loop
- How the `write_todos` tool keeps a long task on track
- How filesystem tools prevent context overflow
- How to spawn subagents for parallel, isolated work
- How to add your own tools alongside the built-ins

**[→ Start DeepAgent module](DeepAgent/README.md)**

---

## Project Structure

```
ai-agent-systems-course/
├── MCP/                             # Module 1 — LLMs calling tools
│   ├── docs/                        # 6 teaching documents (read first)
│   ├── examples/                    # 4 runnable examples (calculator → database)
│   ├── exercises/                   # Hands-on tasks
│   └── solutions/                   # Exercise answers
├── A2A/                             # Module 2 — agents calling agents
│   ├── docs/                        # 10 teaching documents (read first)
│   ├── remote_math_agent.py         # Math specialist (port 8001)
│   ├── remote_prime_agent.py        # Prime checker specialist (port 8003)
│   ├── coordinator_agent.py         # Static coordinator
│   ├── dynamic_coordinator_agent.py # Dynamic coordinator (registry-based)
│   └── registry_server.py           # Agent registry (port 8004)
├── DeepAgent/                       # Module 3 — single agent harness
│   ├── docs/                        # 4 teaching documents (read first)
│   ├── examples/                    # 3 runnable examples
│   ├── llm_config.py                # LLM provider abstraction
│   ├── .env.example                 # Copy to .env, fill in credentials
│   └── requirements.txt
└── README.md                        # This file
```

---

## Prerequisites

- **Python 3.10 or newer** (Python 3.11+ for DeepAgent)
- **MCP module:** No prior AI or MCP knowledge needed. Basic Python is enough.
- **A2A module:** Requires an API key for Azure OpenAI or Google Gemini. See [A2A Environment Setup](A2A/docs/05-environment-setup.md).
- **DeepAgent module:** Requires an API key for OpenAI, Azure OpenAI, or Google Gemini (or a local Ollama instance).

**Windows users:** See [MCP Windows Setup](MCP/docs/06-windows-setup.md) for Git, Python, and VS Code installation.

---

## License

See [MCP/LICENSE](MCP/LICENSE) for the MCP module. A2A materials follow the same terms.
