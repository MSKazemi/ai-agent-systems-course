# Section 8 — A2A Client (Hands-on)

In the previous section we exposed our agent as an **A2A server**.

Now we will create a **client agent** that can send tasks to another agent.

This demonstrates the core idea of A2A:

> **Agents can call other agents just like services call APIs.**
> 

---

# Step 1 — A2A Client Concept

An **A2A client** is simply an agent (or application) that sends a **task request** to another agent.

Architecture:

```
Client Agent
     │
     │ A2A request
     ▼
Agent Server
     │
     ▼
Agent Runtime
```

The client:

1️⃣ creates a task

2️⃣ sends the task to the server

3️⃣ receives the result

---

# Step 2 — Create a Simple Client Script

Create a file:

```
client.py
```

Example client:

```python
import requests

response = requests.post(
    "http://localhost:8000/invoke",
    json={
        "message": "What time is it in Rome?"
    }
)

print(response.json())
```

Run:

```
python client.py
```

The client sends a request to the agent server and receives the response.

---

# Step 3 — Task Creation

A **task** represents work that an agent should perform.

Example task:

```python
task = {
    "message": "What time is it in Rome?"
}
```

The client sends this task to the server.

In real A2A systems tasks may also include:

- task ID
- metadata
- conversation context

---

# Step 4 — Message Format

The **message** contains the content of the request.

Example:

```python
{
  "message": "Summarize this document"
}
```

More advanced systems may include structured messages such as:

```python
{
  "role": "user",
  "content": "Summarize this document"
}
```

This allows agents to support **multi-turn conversations**.

---

# Step 5 — Full Interaction Flow

Here is the complete interaction:

```
Client Agent
      │
      │ POST /invoke
      ▼
A2A Server
      │
      │ create task
      ▼
Agent Runtime
      │
      │ process task
      ▼
Response returned
```

---

# Example Response

The server returns a result:

```json
{
  "response": "The current time in Rome is 10:30 AM."
}
```

The client prints the result.

---

# What Students Learn

After this exercise students understand:

- how to **send tasks between agents**
- how A2A uses **standard HTTP endpoints**
- how agents exchange **messages**

They also see that **A2A communication is very similar to calling an API**.

---

# Teaching Tip (Live Demo)

Run these side-by-side:

Terminal 1:

```
adk api_server --a2a
```

Terminal 2:

```
python client.py
```

Students will see:

1️⃣ client sends request

2️⃣ server processes task

3️⃣ response returned

This helps them visualize **agent-to-agent communication**.

---

[← Previous: Section 7](07-expose-agent-a2a.md) | [Next: Section 9 — Agent Orchestration →](09-agent-orchestration.md)
