# Section 4 — DeepAgent vs MCP vs A2A

This course covers three technologies. They are complementary, not competing. This doc explains where each one fits.

---

## The Three Layers

```
┌─────────────────────────────────────────────────────┐
│                  DeepAgent                          │
│   Agent harness: planning, context, subagents       │
│   "How does a single agent handle complex tasks?"   │
├─────────────────────────────────────────────────────┤
│                    A2A                              │
│   Agent-to-agent protocol: discovery, delegation    │
│   "How do multiple agents communicate?"             │
├─────────────────────────────────────────────────────┤
│                    MCP                              │
│   Model Context Protocol: tool exposure             │
│   "How does an LLM call a function?"                │
└─────────────────────────────────────────────────────┘
```

Each layer solves a different problem.

---

## Side-by-Side Comparison

| Question | MCP | A2A | DeepAgent |
|---|---|---|---|
| What problem does it solve? | LLM ↔ tool communication | Agent ↔ agent communication | Single agent infrastructure |
| Who uses it? | LLM + tool server | Coordinator + remote agents | One agent with complex tasks |
| Standard or framework? | Open standard (spec) | Open standard (spec) | Open-source framework |
| Transport | SSE / STDIO | HTTP (JSON-RPC) | In-process (LangGraph) |
| Discovery | Via MCP client | Via agent cards | N/A |
| Cross-framework? | Yes | Yes | No (LangChain ecosystem) |
| Subagents? | No | Yes (remote) | Yes (in-process) |
| Planning? | No | No | Yes (`write_todos`) |
| Context management? | No | No | Yes (filesystem tools) |

---

## Mental Models

**MCP** is a *plugin socket*.

> "I have a Python function. I want any LLM to be able to call it."

```
LLM → MCP client → MCP server → your_function()
```

---

**A2A** is a *remote agent bus*.

> "I have agents built in different frameworks. I want them to talk to each other over HTTP."

```
Coordinator (ADK) → A2A → Math Agent (LangGraph)
Coordinator (ADK) → A2A → Research Agent (AutoGen)
```

---

**DeepAgent** is a *task runtime*.

> "I have one agent that needs to do a large, complex task without losing context or forgetting steps."

```
create_deep_agent()
    ├── plan the task
    ├── read/write files as needed
    ├── spawn subagents for parallel work
    └── return the complete result
```

---

## They Work Together

These technologies are not mutually exclusive. A real system might use all three:

```
User
  │
  ▼
DeepAgent (orchestrator harness)
  │  Uses built-in planning + filesystem tools
  │
  ├── MCP tool call → database server (gets live data)
  │
  └── A2A call → specialist agent (different framework)
               running on another machine
```

DeepAgent handles *how the agent works internally*.
A2A handles *how agents talk to each other*.
MCP handles *how an agent calls external tools*.

---

## Decision Guide

Use **MCP** when:
- You want to expose a function/resource to any LLM or AI assistant
- You want to add tools to VS Code, Cursor, Claude Desktop, etc.
- You need cross-framework tool sharing

Use **A2A** when:
- You have agents built in different frameworks that need to communicate
- You want agents discoverable over HTTP with standardized interfaces
- You're building a distributed multi-agent system

Use **DeepAgent** when:
- You need a single agent to handle long, multi-step tasks
- Context window size is a concern
- You want built-in planning and subagent support
- You're building on top of LangChain/LangGraph

---

## This Course at a Glance

| Module | Technology | Core lesson |
|--------|-----------|-------------|
| MCP | Model Context Protocol | LLMs calling your functions |
| A2A | Agent-to-Agent | Agents communicating over HTTP |
| DeepAgent | DeepAgents framework | One agent handling complex tasks |

---

[← Back to README](../README.md)
