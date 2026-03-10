# Section 7 — Expose Agent with A2A (Hands-on)

In the previous section we created a **working ADK agent** and tested it using the Dev UI.

Now we will expose this agent so that **other agents can discover and communicate with it**.

This is where the **A2A protocol becomes useful**.

---

# Step 1 — Start the A2A Server

ADK can automatically expose an agent using the **A2A protocol**.

Run the following command from the project directory:

```bash
adk api_server --a2a
```

This starts an **HTTP server** that exposes your agent using A2A endpoints.

Example server address:

```
http://localhost:8000
```

Now your agent is no longer just a local program — it becomes a **network service that other agents can call**.

---

# Step 2 — A2A Server Endpoints

The A2A server provides several standard endpoints.

| Endpoint | Purpose |
| --- | --- |
| `/agent.json` | Agent metadata (Agent Card) |
| `/invoke` | Execute a task immediately |
| `/tasks` | Manage asynchronous tasks |
| `/health` | Server health status |

These endpoints follow the **A2A protocol specification**.

---

# Step 3 — Inspect the Agent Card

Open a browser and visit:

```
http://localhost:8000/agent.json
```

You should see something like this:

```json
{
  "name": "time_agent",
  "description": "Tells the current time in a city",
  "skills": ["get_current_time"],
  "endpoint": "/tasks"
}
```

This is called the **Agent Card**.

It tells other agents:

- what the agent does
- what skills it provides
- how to send tasks

---

# Step 4 — Check Server Health

You can also check if the server is running:

```
http://localhost:8000/health
```

Example response:

```json
{
  "status": "ok"
}
```

This is useful for monitoring and orchestration systems.

---

# Step 5 — Call the Agent (Optional Demo)

We cannot easily call `/invoke` from a browser because it requires a **POST request**.

Instead we can use Python.

Example:

```python
import requests

response = requests.post(
    "http://localhost:8000/invoke",
    json={"message": "What time is it in Rome?"}
)

print(response.json())
```

The agent processes the request and returns the result.

---

# What Just Happened?

Before:

```
User → ADK agent
```

Now:

```
Agent Client
      │
      │ A2A
      ▼
Your ADK Agent Server
```

Your agent is now **discoverable and callable by other agents**.

---

# Architecture After This Step

```
Agent Client
      │
      │ A2A
      ▼
ADK API Server
      │
      ▼
Agent Runtime
```

Where:

| Component | Role |
| --- | --- |
| Agent Client | sends tasks |
| ADK API Server | handles A2A protocol |
| Agent Runtime | executes logic |

---

# Key Learning Outcome

Students now understand that:

- a normal agent can become an **A2A server**
- the server exposes **standard endpoints**
- other agents can discover it using **agent cards**

---

# Quick Live Demo Idea

In class you can do this:

1️⃣ Run the server

```
adk api_server --a2a
```

2️⃣ Open:

```
http://localhost:8000/agent.json
```

3️⃣ Ask students:

> "If another agent reads this file, what can it learn?"
> 

Students usually answer:

- the agent name
- its skills
- how to call it

That helps them understand **agent discovery**.

---

[← Previous: Section 6](06-build-first-agent.md) | [Next: Section 8 — A2A Client →](08-a2a-client.md)
