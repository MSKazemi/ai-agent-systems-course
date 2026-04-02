# Section 1 — What is DeepAgent?

## The Starting Point: A Basic LLM Agent

You already know how a basic agent works from the MCP and A2A modules:

```
User message
    │
    ▼
LLM decides which tool to call
    │
    ▼
Tool runs, returns result
    │
    ▼
LLM reads result, decides next step
    │
    ▼
Repeat until done
```

This loop works for simple tasks.

---

## The Problem: What Breaks at Scale

Imagine you ask an agent to:

> "Read all Python files in this project, identify which ones have no tests, write tests for each one, and produce a summary report."

Three things break immediately:

### 1. Context Overflow

The LLM has a limited context window. Loading dozens of files fills it up fast. The agent crashes or starts forgetting earlier content.

### 2. No Plan

The agent has no way to track "what have I done so far?" and "what's left?". It might repeat work or miss steps.

### 3. No Parallelism

Writing tests for 20 files sequentially is slow. Ideally you'd delegate each file to a specialist agent running in its own context.

---

## What DeepAgent Is

DeepAgent is an **agent harness** — a framework that wraps the basic agent loop and adds the missing infrastructure.

It was built by the LangChain team, is fully open-source (MIT), and runs on **LangGraph** under the hood.

```
Your code
    │
    ▼
create_deep_agent()  ← DeepAgent harness
    │
    ├── LLM (your choice)
    ├── Built-in tools (planning, filesystem, subagents, shell)
    └── LangGraph runtime (streaming, persistence, human-in-the-loop)
```

You write the goal. DeepAgent handles the infrastructure.

---

## The "Batteries Included" Analogy

| Without DeepAgent | With DeepAgent |
|---|---|
| You manage context manually | Filesystem tools offload data automatically |
| No built-in planning | `write_todos` tool tracks progress |
| You build subagent logic | `task` tool spawns isolated subagents |
| You configure LangGraph | It's already wired in |

---

## What DeepAgent Is NOT

- It is not an LLM. You bring your own LLM (OpenAI, Gemini, Ollama, etc.)
- It is not a hosted service. It runs locally in your Python environment
- It is not a replacement for MCP or A2A. It solves a different layer of the problem (more on this in doc 04)

---

## A Real-World Mental Model

Think of DeepAgent like a **senior engineer**.

A junior engineer (basic agent) can do one task at a time and has to keep everything in their head.

A senior engineer (DeepAgent) can:
- Break a large project into a checklist
- Write notes and files to avoid forgetting
- Delegate subtasks to teammates
- Come back to a paused task later

---

## The Core API

DeepAgent has one main function:

```python
from deepagents import create_deep_agent

agent = create_deep_agent()

result = agent.invoke({
    "messages": [{"role": "user", "content": "Your goal here"}]
})
```

That's it. The agent gets the built-in tools automatically.

You can customize:
- **model** — any LangChain-compatible LLM
- **tools** — add your own Python functions
- **system_prompt** — change the agent's behavior

---

## Summary

| Concept | What it means |
|---|---|
| Agent harness | A framework that wraps the agent loop with real-world infrastructure |
| Built-in tools | Planning, filesystem, subagents, shell — ready to use |
| LangGraph runtime | Streaming, persistence, checkpointing — under the hood |
| Model-agnostic | Works with any LLM that supports tool calling |

---

[Next: Section 2 — Core Concepts →](02-core-concepts.md)
