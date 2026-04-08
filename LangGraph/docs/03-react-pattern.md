# 03 — The ReAct Pattern

**ReAct = Reason + Act**

ReAct is the loop that almost every practical agent uses. The LLM alternates between reasoning about what to do and calling a tool (acting), observing the result, then reasoning again — until it has a final answer.

---

## The loop

```
Think: "I need to multiply 6 × 7. I'll call multiply(6, 7)."
  ↓
Act: multiply(6, 7)  →  42
  ↓
Observe: "The result is 42."
  ↓
Think: "I have the answer. I'll return it."
  ↓
Answer: "6 × 7 = 42"
```

In LangGraph terms:

```
agent node  →  (tool call in response?)  →  tool node  →  agent node
                      ↓ no
                     END
```

---

## Why this matters for DeepAgent

DeepAgent's `create_deep_agent()` builds this exact graph internally, with one addition: it also gives the agent **built-in tools** for managing long tasks:

| Tool | What it does |
|------|-------------|
| `write_todos` | Track a multi-step plan |
| `read_file` / `write_file` / `edit_file` | Persist context to disk |
| `ls` / `glob` / `grep` | Explore a filesystem |
| `execute` | Run shell commands |
| `task` | Spawn an isolated child agent |

These tools let the agent manage work that's too large for a single context window.

---

## The full picture

```
create_deep_agent(model, tools, system_prompt)
       │
       └── builds a LangGraph StateGraph
               ├── agent node  (your LLM + system_prompt)
               ├── tools node  (built-ins + your custom tools)
               └── loop until no more tool calls
```

When you call `agent.invoke({"messages": [...]})`, you're running this graph.

---

## What to look for in the DeepAgent examples

- `get_llm_model()` — picks the LLM (same pattern as this module)
- `create_deep_agent(model=llm, tools=[...])` — builds the ReAct graph
- `agent.invoke({"messages": [...]})` — runs the loop
- `result["messages"][-1].content` — the final answer

Once you see how the graph works, the examples are obvious. Move on to [DeepAgent →](../../DeepAgent/README.md).
