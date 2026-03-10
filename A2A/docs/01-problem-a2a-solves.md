# Section 1 — The Problem A2A Solves

## Motivation

Today many frameworks allow us to build **AI agents**:

- LangGraph
- Google ADK
- AutoGen
- CrewAI

Each framework can create powerful agents that:

- answer questions
- search information
- call tools
- coordinate workflows

But there is a **big problem**.

Agents built in **different frameworks cannot easily talk to each other**.

---

## Example Scenario

Imagine a company building an AI system.

They have:

| Agent | Framework | Purpose |
| --- | --- | --- |
| Research Agent | LangGraph | search documents |
| Coordinator Agent | Google ADK | manage workflow |
| Math Agent | AutoGen | perform calculations |

Ideally the system should work like this:

```
User
 │
 ▼
Coordinator Agent
 │
 ├── Research Agent
 └── Math Agent
```

But because each framework works differently, **agents cannot communicate directly**.

---

# The Reality Without A2A

Developers must write **custom integrations**.

Example architecture:

```
Agent A → custom API → Agent B
Agent C → custom API → Agent D
```

Each connection requires:

- new API design
- custom message format
- custom authentication
- custom documentation

As systems grow, integration becomes messy.

---

## Resulting Problems

### Fragmentation

Every framework has its own communication system.

Example:

- LangGraph uses one format
- AutoGen uses another
- ADK uses another

Nothing is standardized.

---

### Framework Lock-in

If your company builds many agents using one framework:

You become **dependent on that ecosystem**.

Example problem:

> "Our agents only work with LangGraph."
> 

---

### Integration Complexity

If you have **10 agents**, you might need many custom connections.

Example:

```
Agent A ↔ Agent B
Agent A ↔ Agent C
Agent B ↔ Agent D
Agent C ↔ Agent D
```

This becomes difficult to maintain.

---

# Simple Python Example (Without A2A)

Let's simulate **two agents built independently**.

### Research Agent (Server)

```python
# research_agent.py

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/search", methods=["POST"])
def search():
    query = request.json["query"]

    result = f"Research results for: {query}"

    return jsonify({"result": result})

app.run(port=5001)
```

This agent exposes a **custom API endpoint**.

---

### Coordinator Agent (Client)

```python
# coordinator_agent.py

import requests

query = "A2A protocol"

response = requests.post(
    "http://localhost:5001/search",
    json={"query": query}
)

print(response.json())
```

Output:

```
{'result': 'Research results for: A2A protocol'}
```

---

## What is the Problem Here?

This integration works, but:

- The API endpoint `/search` is **custom**
- The message format `{query: ...}` is **custom**
- Another agent might use `{message: ...}` instead

So every integration requires **manual coordination**.

---

# Now Imagine Many Agents

Example system:

```
Coordinator Agent
 │
 ├── Research Agent
 ├── Math Agent
 ├── Calendar Agent
 └── Report Agent
```

Each agent might have a **different API**.

Developers must constantly write **translation code**.

---

# The Solution: A2A Protocol

The **Agent2Agent (A2A) Protocol** was announced by Google in April 2025.

Its goal is simple:

> Define a **standard way for AI agents to discover and communicate with each other**.
> 

Instead of custom APIs:

```
Agent A → A2A → Agent B
```

All agents follow the **same communication model**.

---

## What A2A Standardizes

A2A defines how agents:

### Discover agents

Agents publish a description called an **Agent Card**.

Example:

```
http://agent-server/agent.json
```

---

### Send tasks

Agents request work from other agents.

Example:

```
POST /tasks
```

---

### Exchange messages

Agents send structured messages.

---

### Return results

Agents return results called **artifacts**.

---

# Key Idea

Think of A2A like this:

| Technology | Purpose |
| --- | --- |
| HTTP | communication between web services |
| REST | standardized API format |
| **A2A** | standardized communication between AI agents |

So we can say:

> **A2A is like HTTP for AI agents.**
> 

---

# Visual Summary

Without A2A:

```
Agent A → custom API → Agent B
Agent C → custom API → Agent D
```

With A2A:

```
Agent A
   │
   │ A2A
   ▼
Agent B
```

Any compliant agent can communicate with another.

The core issue is **interface mismatch**—each framework uses different interfaces—not networking itself.

---

# Best Simple Python Example (No frameworks)

Imagine two agents built by two teams.

### Agent built by Team A

```python
class ResearchAgent:

    def run(self, query):
        return f"Research results for: {query}"
```

---

### Agent built by Team B

```python
class MathAgent:

    def calculate(self, expression):
        # Simplified for illustration; use a proper expression parser in production
        return eval(expression)
```

---

### Coordinator tries to use both

```python
research = ResearchAgent()
math = MathAgent()

print(research.run("A2A protocol"))
print(math.calculate("3 + 5"))
```

Works fine.

---

# Now imagine different frameworks

Each framework defines **different interfaces**.

Example:

```python
class LangGraphAgent:

    def invoke(self, input):
        return f"LangGraph response: {input}"
```

---

Another framework:

```python
class ADKAgent:

    def execute(self, message):
        return f"ADK response: {message}"
```

---

Now the coordinator must know **how each framework works**.

```python
agent1 = LangGraphAgent()
agent2 = ADKAgent()

print(agent1.invoke("hello"))
print(agent2.execute("hello"))
```

This becomes messy quickly.

---

# The Real Problem

Each framework defines different methods:

| Framework | Method |
| --- | --- |
| LangGraph | `invoke()` |
| ADK | `execute()` |
| AutoGen | `chat()` |
| CrewAI | `run()` |

A coordinator must know **all these differences**.

---

# The Idea Behind A2A

A2A defines **one standard interface**.

Example conceptually:

```python
class A2AAgent:

    def handle_task(self, message):
        pass
```

Now every agent follows the **same communication protocol**.

Coordinator example:

```
agent.send_task("summarize this text")
```

No matter what framework created the agent.

---

[Next: Section 2 — A2A Core Concepts →](02-a2a-core-concepts.md)
