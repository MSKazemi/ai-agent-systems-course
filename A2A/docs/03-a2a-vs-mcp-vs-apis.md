# Section 3 — A2A vs MCP vs APIs

Modern AI systems often combine **multiple communication protocols**.

Students frequently confuse three important concepts:

- **REST APIs**
- **Model Context Protocol (MCP)**
- **Agent-to-Agent Protocol (A2A)**

Each one solves **a different problem** in the AI ecosystem.

---

# The Three Communication Layers

| Protocol | Who communicates | Purpose |
| --- | --- | --- |
| REST API | Application ↔ Application | General service communication |
| MCP | LLM ↔ Tools | Allow models to use tools safely |
| A2A | Agent ↔ Agent | Enable collaboration between agents |

Think of them as **different layers in an AI system**.

---

# 1️⃣ REST APIs

REST APIs are the **traditional way software systems communicate**.

Example: a web application calling a database service.

### Simple Python Example

```python
import requests

response = requests.get("https://api.weather.com/today")

print(response.json())
```

Architecture:

```
Application
    │
    │ REST API
    ▼
Service
```

REST APIs are **not designed specifically for AI agents**.

They are **general-purpose service interfaces**.

---

# 2️⃣ MCP (Model Context Protocol)

MCP connects **LLMs to tools and external data sources**.

It standardizes how models:

- call tools
- read resources
- execute actions

Example tools:

- database queries
- filesystem access
- web search
- code execution

---

### Example MCP Tool

```python
def get_weather(city: str):
    return f"The weather in {city} is sunny"
```

The LLM can call the tool like this:

```
LLM
 │
 │ MCP
 ▼
Tool: get_weather()
```

Architecture:

```
LLM
 │
 │ MCP
 ▼
Tools / resources
```

MCP focuses on **tool access**, not agent collaboration.

---

# 3️⃣ A2A (Agent-to-Agent Protocol)

A2A enables **agents to collaborate with other agents**.

Instead of calling tools, an agent can call **another agent with specialized capabilities**.

Example:

- research agent
- math agent
- summarization agent
- coding agent

---

### Conceptual Example

```python
task = {
    "message": "Summarize this research paper"
}

agent.send_task(task)
```

Architecture:

```
Agent A
   │
   │ A2A
   ▼
Agent B
```

Agent B processes the task and returns results.

---

# Putting Everything Together

Modern AI systems often use **all three protocols together**.

Example architecture:

```
User
 │
 ▼
Coordinator Agent
 │
 │ A2A
 ▼
Research Agent
 │
 │ MCP
 ▼
Tools / databases
```

---

### What Happens Here?

1️⃣ The **Coordinator Agent** receives a user request.

2️⃣ It sends a task to a **Research Agent** using **A2A**.

3️⃣ The Research Agent uses **MCP** to access tools such as:

- search engines
- databases
- APIs

4️⃣ The results are returned to the coordinator.

---

# Another Realistic Example

Imagine a **travel assistant system**.

```
User
 │
 ▼
Travel Planner Agent
 │
 ├── A2A → Flight Agent
 ├── A2A → Hotel Agent
 └── A2A → Weather Agent
```

Inside each agent:

```
Weather Agent
     │
     │ MCP
     ▼
Weather API
```

So the system works like this:

```
Agents collaborate via A2A
Agents use tools via MCP
Services communicate via APIs
```

---

# Key Insight for Students

The three protocols operate at **different layers**.

| Layer | Technology |
| --- | --- |
| Application layer | REST APIs |
| Tool layer | MCP |
| Agent collaboration layer | A2A |

---

# Visual Summary

Without protocols:

```
Agent → custom APIs → tools
Agent → custom APIs → other agents
```

With modern standards:

```
Agent A
   │
   │ A2A
   ▼
Agent B
   │
   │ MCP
   ▼
Tools / APIs
```

---

# Key Takeaway

| Protocol | Role |
| --- | --- |
| REST API | communication between software services |
| MCP | allows LLMs to safely use tools |
| A2A | allows AI agents to collaborate |

Together they form the **foundation of modern agent architectures**.

---

[← Previous: Section 2](02-a2a-core-concepts.md) | [Next: Section 4 — A2A Architecture →](04-a2a-architecture.md)
