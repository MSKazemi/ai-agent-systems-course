# Section 2 — A2A Core Concepts

In the previous section we learned **why A2A exists**.

Now we will learn the **main building blocks of the A2A protocol**.

A2A defines **a standard structure for communication between agents**.

Think of it like a **language agents use to talk to each other**.

---

# A2A Key Objects

## 1. Agent

An **Agent** is an AI system that can perform tasks.

Examples:

- research agent
- math agent
- summarization agent
- monitoring agent

Example (conceptual Python agent):

```python
class ResearchAgent:

    def handle_task(self, task):
        query = task["message"]
        return f"Research result for: {query}"
```

The agent receives a **task** and produces a **result**.

---

# 2. Agent Card

Before communicating, agents must **describe themselves**.

This description is called an **Agent Card**.

It tells other agents:

- who the agent is
- what it can do
- how to contact it

Example:

```json
{
  "name": "research-agent",
  "description": "Search and summarize information",
  "skills": ["search", "summarize"],
  "endpoint": "http://localhost:8000/tasks"
}
```

This is usually available at:

```
/agent.json
```

Other agents use it to **discover capabilities**.

---

# 3. Skill

A **Skill** describes what an agent can do.

Examples:

| Agent | Skills |
| --- | --- |
| Research agent | search papers |
| Math agent | solve equations |
| Report agent | generate summaries |

Example:

```python
skills = ["search", "summarize"]
```

The agent card exposes these skills so others know **when to call the agent**.

---

# 4. Task

A **Task** represents a unit of work sent to an agent.

Example tasks:

- summarize this document
- compute a result
- search for papers

Example task message:

```python
task = {
    "id": "task_1",
    "message": "Find papers about A2A protocol"
}
```

The receiving agent will process this task.

---

# 5. Message

A **Message** carries the communication content.

Example message:

```python
message = {
    "role": "user",
    "content": "Summarize this article"
}
```

Messages allow agents to have **multi-step conversations**.

---

# 6. Artifact

An **Artifact** is the **output produced by the agent**.

Examples:

- a text answer
- a document
- structured data
- a file

Example:

```python
artifact = {
    "type": "text",
    "content": "Summary of the article..."
}
```

Artifacts are returned to the requesting agent.

---

# 7. Part

A **Part** represents a structured piece of content inside messages.

Example:

A message could contain:

- text
- images
- files

Example:

```python
part = {
    "type": "text",
    "data": "Explain A2A protocol"
}
```

A message can contain multiple parts.

---

# A2A Lifecycle

Now let's see **how agents actually interact**.

The A2A protocol defines a **standard lifecycle**.

---

## 1. Discovery

Agent A first **discovers another agent**.

It reads the **Agent Card**.

Example:

```
GET /agent.json
```

Response:

```
{
  "name": "research-agent",
  "skills": ["search"]
}
```

Agent A now knows **what Agent B can do**.

---

## 2. Task Creation

Agent A sends a **task request**.

Example:

```python
task = {
    "id": "task1",
    "message": "Search papers about AI agents"
}
```

---

## 3. Processing

Agent B receives the task and processes it.

Example:

```python
def handle_task(task):
    query = task["message"]
    return f"Results for {query}"
```

---

## 4. Interaction (Optional)

Sometimes agents may **exchange multiple messages**.

Example:

Agent B asks for clarification:

```
Agent B → Agent A
"Do you want academic papers or blog posts?"
```

This allows **multi-turn collaboration**.

---

## 5. Completion

Finally the agent returns **artifacts**.

Example:

```python
artifact = {
    "type": "text",
    "content": "Top papers on A2A protocol..."
}
```

This completes the task.

---

# Full Example Interaction

```
Agent A
   │
   │ discover
   ▼
Agent B (agent card)
   │
   │ create task
   ▼
Agent B processes task
   │
   │ optional interaction
   ▼
Artifacts returned
```

---

# Simple Conceptual Python Flow

Here is a **very simplified A2A-like interaction**.

```python
class AgentB:

    def handle_task(self, task):
        query = task["message"]
        return {"artifact": f"Results for {query}"}

agent_b = AgentB()

task = {"message": "Find papers about A2A"}

result = agent_b.handle_task(task)

print(result)
```

Output:

```
{'artifact': 'Results for Find papers about A2A'}
```

This demonstrates the **basic idea of task → processing → artifact**.

---

# Key Takeaway

A2A standardizes **how agents communicate**.

Instead of custom APIs, agents exchange structured objects:

| Object | Role |
| --- | --- |
| Agent Card | describes agent |
| Task | work request |
| Message | communication |
| Artifact | result |

---

[← Previous: Section 1](01-problem-a2a-solves.md) | [Next: Section 3 — A2A vs MCP vs APIs →](03-a2a-vs-mcp-vs-apis.md)
