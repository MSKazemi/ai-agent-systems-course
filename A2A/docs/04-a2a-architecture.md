# Section 4 — A2A Architecture

Now that we understand the **concepts of A2A**, we need to understand **how agents communicate in practice**.

A2A follows a **client–server architecture**, similar to how web systems work.

---

# Client–Server Model

In A2A communication, two main roles exist:

| Role | Description |
| --- | --- |
| **A2A Client** | Agent requesting work |
| **A2A Server** | Agent performing the work |

So one agent **calls another agent**.

---

# A2A Server

An **A2A Server** hosts an agent and exposes its capabilities to other agents.

The server provides several things:

### Agent Card

Describes the agent.

Example:

```
GET /agent.json
```

This tells other agents:

- agent name
- skills
- endpoints

---

### Task Execution

Agents can send tasks to the server.

Example:

```
POST /tasks
```

The server receives the task and sends it to the agent runtime.

---

### Streaming Updates (Optional)

Some tasks take time.

The server can send **progress updates**.

Example:

```
Task started
Searching documents...
Generating summary...
Task completed
```

---

# A2A Client

An **A2A Client** is an agent that wants another agent to perform a task.

Example situations:

- coordinator agent calling a research agent
- planner agent calling a math agent
- monitoring agent calling a diagnosis agent

The client:

1. discovers the agent
2. sends a task
3. receives the result

---

# A2A Architecture

The interaction looks like this:

```
Agent Client
      │
      │ A2A request
      ▼
A2A Server
      │
      ▼
Agent Runtime
```

Where:

| Component | Role |
| --- | --- |
| Client | sends task |
| Server | exposes endpoints |
| Runtime | executes agent logic |

---

# Task Flow in A2A

A typical interaction follows these steps.

```
Agent Client
      │
      │ 1. Discover agent
      ▼
A2A Server
      │
      │ 2. Create task
      ▼
Agent Runtime
      │
      │ 3. Process task
      ▼
Artifact returned
```

---

# Simple Python Simulation

To understand the architecture, let's simulate it in Python.

### Agent Runtime

```python
class ResearchAgent:

    def handle_task(self, task):
        query = task["message"]
        return f"Results for: {query}"
```

This represents the **agent logic**.

---

### A2A Server

```python
class A2AServer:

    def __init__(self, agent):
        self.agent = agent

    def create_task(self, task):
        return self.agent.handle_task(task)
```

The server receives the task and forwards it to the agent.

---

### A2A Client

```python
class A2AClient:

    def send_task(self, server, task):
        return server.create_task(task)
```

The client sends the task to the server.

---

### Full Example

```python
agent = ResearchAgent()
server = A2AServer(agent)
client = A2AClient()

task = {"message": "Find papers about A2A protocol"}

result = client.send_task(server, task)

print(result)
```

Output:

```
Results for: Find papers about A2A protocol
```

This example demonstrates the **basic A2A architecture**:

- client sends task
- server receives it
- agent processes it
- result returned

---

# Mapping This to Real A2A Systems

In real systems:

| Concept | Real Implementation |
| --- | --- |
| A2A Client | agent making request |
| A2A Server | HTTP service |
| Agent Runtime | framework (ADK, LangGraph, etc.) |

Example:

```
Coordinator Agent
      │
      │ A2A
      ▼
Research Agent Server
      │
      ▼
Research Agent Runtime
```

---

# Key Takeaway

A2A separates **communication from agent logic**.

| Layer | Role |
| --- | --- |
| Client | sends request |
| Server | handles protocol |
| Runtime | executes agent |

This separation allows agents from **different frameworks** to communicate.

---

[← Previous: Section 3](03-a2a-vs-mcp-vs-apis.md) | [Next: Section 5 — Environment Setup →](05-environment-setup.md)
