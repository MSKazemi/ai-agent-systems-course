# Section 3 — Architecture

## The Full Picture

```
Your Python code
        │
        │  create_deep_agent(model, tools, system_prompt)
        ▼
┌─────────────────────────────────────────────────────┐
│                   DeepAgent Harness                 │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │              LangGraph Runtime               │  │
│  │  (streaming · checkpointing · persistence)   │  │
│  └────────────────────┬─────────────────────────┘  │
│                        │                            │
│  ┌─────────────────────▼────────────────────────┐  │
│  │              Agent Loop (ReAct)               │  │
│  │                                               │  │
│  │  LLM ←──── system prompt + tool schemas      │  │
│  │   │                                           │  │
│  │   └──── tool call ──► Tool Executor           │  │
│  │                           │                   │  │
│  │   ◄──── tool result ──────┘                   │  │
│  └───────────────────────────────────────────────┘  │
│                                                     │
│  Built-in Tools                   Custom Tools      │
│  ┌─────────────┐                 ┌──────────────┐  │
│  │ write_todos │                 │ your_tool()  │  │
│  │ read_file   │                 │ another()    │  │
│  │ write_file  │                 └──────────────┘  │
│  │ edit_file   │                                   │
│  │ ls / glob   │    Filesystem Backend             │
│  │ grep        │    ┌──────────────────────────┐   │
│  │ execute     │    │ in-memory / disk /        │   │
│  │ task ───────┼────►  LangGraph store /        │   │
│  └─────────────┘    │  sandbox                  │   │
│                     └──────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## The Agent Loop (ReAct Pattern)

DeepAgent uses the **ReAct** pattern: **Re**ason + **Act**.

```
Step 1: LLM reasons about the task
         "I need to find all Python files, then read each one..."

Step 2: LLM calls a tool
         ls(".")  →  ["agent.py", "config.py", "tests/"]

Step 3: LLM reads the result, reasons again
         "I found 2 files. Let me read agent.py first..."

Step 4: LLM calls another tool
         read_file("agent.py")  →  "def run(): ..."

Step 5: Repeat until the task is complete
```

This loop runs automatically inside `agent.invoke()`.

---

## The LangGraph Runtime

LangGraph is the execution engine under DeepAgent. It provides:

| Feature | What it means |
|---------|---------------|
| **Streaming** | You see the agent's output token-by-token, not all at once |
| **Checkpointing** | The agent's state is saved after each step |
| **Persistence** | Conversations can be resumed after a crash |
| **Human-in-the-loop** | You can pause the agent and inject a message |

You don't have to configure any of this. DeepAgent wires it up.

### Streaming example

```python
agent = create_deep_agent(model=llm)

# Stream output as it arrives
for chunk in agent.stream({
    "messages": [{"role": "user", "content": "Summarize this codebase"}]
}):
    print(chunk, end="", flush=True)
```

---

## How Subagents Work

When the agent calls the `task` tool, DeepAgent creates a **new agent instance** with its own isolated state:

```
Orchestrator Agent (context: 2k tokens)
    │
    │  task("Write tests for auth.py")
    │
    ▼
Child Agent 1 (context: 0 tokens — fresh start)
    ├── reads auth.py
    ├── writes tests
    └── returns result → Orchestrator
```

The child agent:
- Has access to the same built-in tools
- Does NOT share context with the orchestrator
- Can itself spawn grandchild agents (recursive)

This is how DeepAgent avoids context overflow on large tasks.

---

## The Filesystem Abstraction

All filesystem tools go through a **backend interface**. This means you can swap storage without changing the agent's behavior.

```python
# Default: in-memory (nothing persisted to disk)
agent = create_deep_agent()

# Local disk (files saved to ./workspace/)
from deepagents.filesystem import LocalFilesystem
agent = create_deep_agent(filesystem=LocalFilesystem("./workspace"))
```

The agent code is identical either way — it just calls `read_file()` and `write_file()`.

---

## Request Lifecycle: Step by Step

Here is what happens when you call `agent.invoke(...)`:

```
1. Your code calls agent.invoke({"messages": [...]})

2. LangGraph initializes a new thread (or resumes a saved one)

3. The system prompt + tool schemas are prepended to the message

4. The LLM receives: system prompt + tool schemas + your message

5. The LLM outputs either:
   a. A tool call → DeepAgent executes the tool and feeds the result back
   b. A plain text response → the loop ends

6. Steps 4–5 repeat until the LLM stops calling tools

7. The final LLM response is returned to your code
```

---

## Customization Points

```python
from deepagents import create_deep_agent
from langchain_core.tools import tool

@tool
def my_tool(input: str) -> str:
    """My custom tool."""
    return f"Result: {input}"

agent = create_deep_agent(
    model=my_llm,               # any LangChain chat model
    tools=[my_tool],            # added alongside built-in tools
    system_prompt="You are a Python expert.",  # prepended to all conversations
)
```

| Parameter | Default | What it controls |
|-----------|---------|------------------|
| `model` | none (required) | Which LLM to use |
| `tools` | `[]` | Additional tools alongside built-ins |
| `system_prompt` | built-in | Agent personality and instructions |
| `filesystem` | in-memory | Where files are stored |

---

[Next: Section 4 — DeepAgent vs MCP vs A2A →](04-deepagent-vs-mcp-a2a.md)
