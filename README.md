# AI Agent Systems Course

A hands-on, self-paced course for building AI agent systems from the ground up.

---

## What Is an AI Agent?

A traditional program follows fixed instructions: input → logic → output.

An **AI agent** is different: it can *decide* what to do next. You give it a goal in natural language, and it figures out which tools to call, in what order, to accomplish that goal. It can call a calculator, search the web, query a database, or even hand off work to another agent — all without you writing explicit step-by-step code.

This course teaches four key technologies that make agents work in practice:

| Technology          | What it does                                                      | Analogy                             |
|---------------------|-------------------------------------------------------------------|-------------------------------------|
| **MCP**             | Gives an LLM access to external tools (calculators, files, DBs)   | A plugin system for AI              |
| **A2A**             | Lets one agent delegate tasks to other specialized agents         | A manager assigning work to experts |
| **LangGraph**       | The graph-based loop that powers agent reasoning                  | The engine inside the agent         |
| **DeepAgent**       | Gives a single agent planning, context management, and subagents  | A senior engineer with a task list  |

---

## Course Modules

### Recommended order: MCP → A2A → LangGraph → DeepAgent

| Module | What You'll Build | Time |
|--------|-------------------|------|
| **[MCP →](MCP/README.md)** | A server that exposes tools (calculator, file reader, database) to LLMs | ~2–3 hours |
| **[A2A →](A2A/README.md)** | Coordinator agent delegating math and prime checks to remote agents | ~2–3 hours |
| **[LangGraph →](LangGraph/README.md)** | The ReAct loop and LangChain basics — prerequisite for DeepAgent | ~45 min |
| **[DeepAgent →](DeepAgent/README.md)** | A single agent that plans, manages context, and spawns subagents | ~1–2 hours |

---

## Quick Setup

> **One virtualenv, one `.env` file — covers every module.**

```bash
# 1. Clone or pull the latest course materials (see "Keeping up to date" below)

# 2. Create and activate the shared virtualenv
python3 -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate

# 3. Install all dependencies
pip install -r requirements.txt

# 4. Configure your LLM provider
cp .env.example .env
# Edit .env — Ollama is the default (runs locally, no API key needed).
# See "LLM providers" below for alternatives.
```

### LLM providers

The course defaults to **Ollama** (local, free, no API key). Set `LLM_PROVIDER` in your `.env`:

| Provider | `LLM_PROVIDER` | Requires |
|----------|---------------|---------|
| Ollama (default) | `ollama` | [Ollama](https://ollama.com) + `ollama pull qwen3.5:35b` |
| Azure OpenAI | `azure` | `AZURE_OPENAI_*` vars in `.env` |
| Google Gemini | `gemini` | `GOOGLE_API_KEY` in `.env` |
| OpenAI | `openai` | `OPENAI_API_KEY` in `.env` (DeepAgent only) |

---

## Keeping up to date

New materials are added each week. Here's how to pull the latest on your platform:

### Linux / macOS

```bash
cd ai-agent-systems-course
git pull origin main
pip install -r requirements.txt   # pick up any new dependencies
```

### Windows (Command Prompt or PowerShell)

```bat
cd ai-agent-systems-course
git pull origin main
.venv\Scripts\activate
pip install -r requirements.txt
```

### Windows (Git Bash)

```bash
cd ai-agent-systems-course
git pull origin main
source .venv/Scripts/activate
pip install -r requirements.txt
```

> **If you have local changes** that conflict with the update:
> ```bash
> git stash          # save your changes temporarily
> git pull origin main
> git stash pop      # restore your changes
> ```

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

## Module 2.5 — LangGraph & LangChain Primer

**The idea:** DeepAgent is built on LangChain and LangGraph. Before jumping into DeepAgent, spend ~45 minutes on the key concepts — chat models, tool binding, state graphs, and the ReAct loop.

**What you'll learn:**

- LangChain's ChatModel interface (same code works with Ollama, OpenAI, Azure, Gemini)
- How to define and bind tools
- What a LangGraph state graph looks like
- The ReAct pattern: reason → act → observe → repeat

**[→ Start LangGraph primer](LangGraph/README.md)**

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
├── .env.example                     # Copy to .env — shared LLM config for all modules
├── requirements.txt                 # One venv covers every module
├── llm_config.py                    # Shared LangChain model config (LangGraph + DeepAgent)
├── MCP/                             # Module 1 — LLMs calling tools
│   ├── docs/                        # 6 teaching documents (read first)
│   ├── examples/                    # 4 runnable examples (calculator → database)
│   ├── exercises/                   # Hands-on tasks
│   ├── solutions/                   # Exercise answers
│   └── llm_config.py                # OpenAI-compatible client for MCP demos
├── A2A/                             # Module 2 — agents calling agents
│   ├── docs/                        # 10 teaching documents (read first)
│   ├── remote_math_agent.py         # Math specialist (port 8001)
│   ├── remote_prime_agent.py        # Prime checker specialist (port 8003)
│   ├── coordinator_agent.py         # Static coordinator
│   ├── dynamic_coordinator_agent.py # Dynamic coordinator (registry-based)
│   ├── registry_server.py           # Agent registry (port 8004)
│   └── llm_config.py                # ADK model config for A2A agents
├── LangGraph/                       # Module 2.5 — LangChain + LangGraph primer
│   ├── docs/                        # 3 focused teaching documents
│   └── examples/                    # 2 hands-on examples
├── DeepAgent/                       # Module 3 — single agent harness
│   ├── docs/                        # 4 teaching documents (read first)
│   ├── examples/                    # 3 runnable examples
│   ├── llm_config.py                # LangChain model config for DeepAgent
│   └── .env.example                 # Module-local override (optional)
└── README.md                        # This file
```

---

## Prerequisites

- **Python 3.10 or newer** (Python 3.11+ recommended)
- **Ollama** (recommended) — download at [ollama.com](https://ollama.com), then:
  ```bash
  ollama pull qwen3.5:35b
  ```
- Or an API key for Azure OpenAI, Google Gemini, or OpenAI (see `.env.example`)

**Windows users:** See [MCP Windows Setup](MCP/docs/06-windows-setup.md) for Git, Python, and VS Code installation.

---

## License

See [MCP/LICENSE](MCP/LICENSE) for the MCP module. All other materials follow the same terms.
