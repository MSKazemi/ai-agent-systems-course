# Module 2.5 — LangChain & LangGraph Primer

**Read this before starting DeepAgent.**

DeepAgent is built on LangChain and LangGraph. This module gives you the minimal mental model you need — no fluff, just the concepts that show up directly in the DeepAgent code.

---

## What you'll learn

| Doc | Topic |
|-----|-------|
| [01 — What is LangChain?](docs/01-what-is-langchain.md) | Chat models, messages, tools, LCEL |
| [02 — What is LangGraph?](docs/02-what-is-langgraph.md) | State, nodes, edges, graphs |
| [03 — The ReAct Pattern](docs/03-react-pattern.md) | How agents think and act in a loop |

**Time: ~45 minutes**

---

## Hands-on examples

```
examples/
├── 01-chain-and-tools/    # LangChain: model + tool binding
└── 02-langgraph-agent/    # LangGraph: minimal ReAct agent
```

### Setup

```bash
# From repo root — one venv covers everything
source .venv/bin/activate          # Windows: .venv\Scripts\activate
cp .env.example .env               # once only — fill in your provider
```

### Run

```bash
# Example 1: LangChain basics
python LangGraph/examples/01-chain-and-tools/example.py

# Example 2: LangGraph ReAct agent
python LangGraph/examples/02-langgraph-agent/agent.py
```

---

## Where this fits

```
MCP  →  A2A  →  [LangGraph primer]  →  DeepAgent
```

After finishing this module, the DeepAgent code will look familiar — you'll recognise the graph, the state, and the tool nodes.
