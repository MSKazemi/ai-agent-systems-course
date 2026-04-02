# DeepAgent — Hands-On Course Module

A self-paced module for building sophisticated AI agents with **DeepAgents** (by LangChain).

---

## What Is DeepAgent?

A traditional LLM agent is just a loop: *call LLM → call tool → repeat*.

**DeepAgent** is a batteries-included harness that wraps that loop and adds what you need for real-world, complex tasks:

| Capability | Built-in tool | What it solves |
|---|---|---|
| Planning | `write_todos` | Breaks large tasks into steps |
| Context management | `read_file`, `write_file`, `edit_file`, `ls` | Keeps context from overflowing |
| Subagent delegation | `task` | Spawns isolated specialist agents |
| Shell execution | `execute` | Runs system commands safely |
| Persistent memory | LangGraph Memory Store | Remembers across sessions |

Think of it as the agent infrastructure you would have to build yourself — already built.

---

## Prerequisites

- Python 3.11+
- An API key for OpenAI, Azure OpenAI, or Google Gemini (or a local Ollama instance)
- Completed the MCP and A2A modules is recommended but not required

---

## Quick Start (5 Minutes)

```bash
cd DeepAgent

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure your LLM provider
cp .env.example .env
# Edit .env and set LLM_PROVIDER + your API key

# Run your first DeepAgent
python examples/01-hello-agent/agent.py
```

---

## Teaching Docs

Read these before running examples. Each doc builds on the previous.

| Doc | Topic |
|-----|-------|
| [01 – What is DeepAgent?](docs/01-what-is-deepagent.md) | The problem it solves, key concepts |
| [02 – Core Concepts](docs/02-core-concepts.md) | Tools, planning, subagents, filesystem |
| [03 – Architecture](docs/03-architecture.md) | How the pieces fit together, LangGraph runtime |
| [04 – DeepAgent vs MCP vs A2A](docs/04-deepagent-vs-mcp-a2a.md) | When to use which technology |

---

## Learning Path

### Phase 1 — Read the docs

| # | Doc |
|---|-----|
| 1 | [01-what-is-deepagent](docs/01-what-is-deepagent.md) |
| 2 | [02-core-concepts](docs/02-core-concepts.md) |
| 3 | [03-architecture](docs/03-architecture.md) |
| 4 | [04-deepagent-vs-mcp-a2a](docs/04-deepagent-vs-mcp-a2a.md) |

### Phase 2 — Hands-on

| # | Example | What you'll see |
|---|---------|-----------------|
| 5 | [01-hello-agent](examples/01-hello-agent) | Minimal agent, default tools, invoke |
| 6 | [02-custom-tools](examples/02-custom-tools) | Add your own Python functions as tools |
| 7 | [03-subagents](examples/03-subagents) | Spawn specialist subagents via `task` |

---

## Examples

| Example | What it shows |
|---------|---------------|
| [01-hello-agent](examples/01-hello-agent) | Create an agent, send a message, print the result |
| [02-custom-tools](examples/02-custom-tools) | Register custom tools and watch the agent use them |
| [03-subagents](examples/03-subagents) | An orchestrator that delegates to isolated subagents |

---

## Project Structure

```
DeepAgent/
├── docs/                          ← Teaching docs (read first)
│   ├── 01-what-is-deepagent.md
│   ├── 02-core-concepts.md
│   ├── 03-architecture.md
│   └── 04-deepagent-vs-mcp-a2a.md
├── examples/
│   ├── 01-hello-agent/            ← Minimal working agent
│   ├── 02-custom-tools/           ← Agent with your own tools
│   └── 03-subagents/              ← Subagent delegation
├── llm_config.py                  ← LLM provider abstraction
├── .env.example                   ← Copy to .env, fill in credentials
├── requirements.txt
└── README.md                      ← This file
```

---

## LLM Provider Setup

Edit `.env` and set `LLM_PROVIDER`:

| Provider | Key(s) needed |
|----------|---------------|
| `openai` (default) | `OPENAI_API_KEY` |
| `azure` | `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_DEPLOYMENT` |
| `gemini` | `GOOGLE_API_KEY` |
| `ollama` | `OLLAMA_MODEL`, `OLLAMA_BASE_URL` (no key needed) |
