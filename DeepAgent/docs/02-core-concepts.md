# Section 2 — Core Concepts

DeepAgent provides four categories of built-in capability. This doc explains each one.

---

## 1. Planning — `write_todos`

### The problem

An LLM without a plan will either:
- Try to do everything at once (context overflow)
- Forget what it already did (repeat work)
- Miss steps (incomplete output)

### The solution

The `write_todos` tool lets the agent create and update a checklist before starting work.

```
Agent receives task: "Write a Python script, test it, and document it"
    │
    ▼
Agent calls write_todos([
    "Write the script",
    "Write the tests",
    "Run the tests",
    "Write the documentation"
])
    │
    ▼
Agent works through each item, checking them off
```

### What this looks like in practice

You do not call `write_todos` yourself. The agent calls it automatically when it detects a multi-step task.

You can observe this in the output when running examples.

---

## 2. Filesystem Tools

### The problem

LLMs have a limited context window. If you load many files, the context fills up and the model starts making mistakes.

### The solution

DeepAgent gives the agent a **virtual filesystem**. Instead of putting all file contents into the prompt, the agent reads files on demand.

| Tool | Purpose |
|------|---------|
| `read_file` | Read a file's contents |
| `write_file` | Create or overwrite a file |
| `edit_file` | Make targeted edits to a file |
| `ls` | List files in a directory |
| `glob` | Find files matching a pattern |
| `grep` | Search for text across files |

### Example

```python
# The agent does this automatically — you don't call these directly

agent.invoke({
    "messages": [{
        "role": "user",
        "content": "Read all .py files and summarize what each one does"
    }]
})

# Under the hood:
#   agent calls ls() → finds ["agent.py", "tools.py", "config.py"]
#   agent calls read_file("agent.py") → reads it
#   agent calls read_file("tools.py") → reads it
#   ...summarizes each one
```

The file contents are never all in context at once.

### Pluggable backends

The filesystem backend is swappable:

| Backend | When to use |
|---------|-------------|
| In-memory (default) | Development, testing |
| Local disk | When you want persistent files |
| LangGraph store | When you want cloud persistence |
| Sandbox | When you want isolated execution |

```python
from deepagents import create_deep_agent
from deepagents.filesystem import LocalFilesystem

agent = create_deep_agent(
    filesystem=LocalFilesystem(base_path="./workspace")
)
```

---

## 3. Subagent Delegation — `task`

### The problem

Some tasks have independent subtasks that don't need to share context. Doing them all in one agent means:
- One long context (slow, expensive)
- Risk of one subtask's output confusing another

### The solution

The `task` tool lets an agent **spawn a child agent** with its own fresh context window.

```
Orchestrator Agent
    │
    ├── task("Write tests for auth.py")    → Child Agent 1
    ├── task("Write tests for db.py")      → Child Agent 2
    └── task("Write tests for api.py")     → Child Agent 3
```

Each child agent:
- Has its own isolated context
- Has access to the same built-in tools
- Returns a result to the orchestrator

### Example

```python
agent.invoke({
    "messages": [{
        "role": "user",
        "content": """
            I have three Python modules: auth.py, db.py, api.py.
            Write unit tests for each one.
        """
    }]
})

# DeepAgent will automatically:
# 1. Call write_todos to plan
# 2. Call task("Write tests for auth.py") → spawns child
# 3. Call task("Write tests for db.py")   → spawns child
# 4. Call task("Write tests for api.py")  → spawns child
# 5. Collect results and combine
```

---

## 4. Shell Execution — `execute`

The `execute` tool runs shell commands inside the agent's environment.

```python
# The agent can do things like:
#   execute("pytest tests/")
#   execute("pip install requests")
#   execute("python script.py")
```

By default, execution happens in-process. You can configure a sandbox for safety.

---

## 5. Persistent Memory

DeepAgent integrates with **LangGraph's Memory Store** to persist information across sessions.

```
Session 1:
  User: "My name is Alice and I prefer Python"
  Agent: [stores this in memory]

Session 2 (new conversation):
  User: "What language should I use for this project?"
  Agent: "Based on your preference for Python..." ← recalled from memory
```

This is optional. By default, each `invoke()` call is stateless.

---

## How the Tools Are Registered

When you call `create_deep_agent()`, DeepAgent automatically registers all built-in tools with the LLM. The LLM sees them in its tool list just like any other tool.

```python
# What you write:
agent = create_deep_agent()

# What DeepAgent registers behind the scenes:
# tools = [write_todos, read_file, write_file, edit_file, ls, glob, grep, execute, task]
```

You can add your own tools alongside these:

```python
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"It is sunny in {city}."

agent = create_deep_agent(tools=[get_weather])
# Now the agent has: all built-in tools + get_weather
```

---

## Summary

| Concept | Tool(s) | What it gives the agent |
|---|---|---|
| Planning | `write_todos` | Step-by-step task tracking |
| Context management | `read_file`, `write_file`, `ls`, `glob`, `grep` | Offload data from context window |
| Subagent delegation | `task` | Isolated parallel execution |
| Shell execution | `execute` | Run real system commands |
| Persistent memory | LangGraph Memory Store | Remember across sessions |

---

[Next: Section 3 — Architecture →](03-architecture.md)
