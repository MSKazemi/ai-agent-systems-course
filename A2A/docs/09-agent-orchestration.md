# Section 9 — Agent Orchestration (Hands-on)

So far we learned:

- how to build an agent
- how to expose it as an **A2A server**
- how to call an agent using a **client**

But real systems usually involve **multiple agents working together**.

This coordination of multiple agents is called **Agent Orchestration**.

---

# What is Agent Orchestration?

Agent orchestration means:

> **Managing how multiple agents collaborate to complete a task.**
> 

Instead of a single agent solving everything, different agents perform **specialized roles**.

Example:

| Agent | Role |
| --- | --- |
| Research agent | search information |
| Math agent | perform calculations |
| Summarizer agent | generate summaries |

This approach improves:

- modularity
- scalability
- reliability

---

# Two Common Orchestration Patterns

There are two main patterns used in multi-agent systems.

| Pattern | Description |
| --- | --- |
| Sequential workflow | agents run one after another |
| Coordinator pattern | a central agent manages tasks |

---

# 1️⃣ Sequential Orchestration

In sequential orchestration, agents run **one after another in a pipeline**.

Architecture:

```
Agent A → Agent B → Agent C
```

Each agent receives the output of the previous agent.

---

## Example Workflow

```
Search Agent → Summarizer Agent → Report Agent
```

Process:

1️⃣ Search agent finds information

2️⃣ Summarizer agent condenses the content

3️⃣ Report agent generates a final report

---

## Simple Python Example

```python
import requests

search_result = requests.post(
    "http://localhost:8001/invoke",
    json={"message": "Find papers about A2A"}
).json()

summary = requests.post(
    "http://localhost:8002/invoke",
    json={"message": search_result}
).json()

report = requests.post(
    "http://localhost:8003/invoke",
    json={"message": summary}
).json()

print(report)
```

Each agent performs **one specialized step**.

---

# Sequential Architecture Diagram

```
User
 │
 ▼
Search Agent
 │
 ▼
Summarizer Agent
 │
 ▼
Report Agent
```

This approach is simple and works well for **linear workflows**.

---

# 2️⃣ Coordinator Pattern

The **coordinator pattern** is the most common architecture in modern agent systems.

Instead of a fixed pipeline, a **central agent decides which agent to call**.

Architecture:

```
User
 │
 ▼
Coordinator Agent
 │
 ├── Research Agent
 ├── Math Agent
 └── Summarizer Agent
```

---

## How It Works

The coordinator agent:

1️⃣ receives the user request

2️⃣ decides which agent should handle the task

3️⃣ sends tasks to the appropriate agents

4️⃣ combines results

---

## Example Scenario

User asks:

```
"What are the top AI research papers and summarize them?"
```

Coordinator logic:

1️⃣ call **research agent**

2️⃣ send results to **summarizer agent**

3️⃣ return final answer

---

## Simple Python Coordinator Example

```python
import requests

def coordinator(question):

    research = requests.post(
        "http://localhost:8001/invoke",
        json={"message": question}
    ).json()

    summary = requests.post(
        "http://localhost:8002/invoke",
        json={"message": research}
    ).json()

    return summary

result = coordinator("Find AI papers and summarize them")

print(result)
```

The coordinator controls the workflow.

---

# Coordinator Architecture

```
User
 │
 ▼
Coordinator Agent
 │
 ├── A2A → Research Agent
 ├── A2A → Math Agent
 └── A2A → Summarizer Agent
```

Each agent specializes in **one capability**.

---

# Why Coordinator Pattern Is Popular

Advantages:

| Advantage | Explanation |
| --- | --- |
| flexible | workflow can change dynamically |
| scalable | easy to add new agents |
| modular | agents remain independent |

Many modern agent systems use this architecture.

Examples:

- planning agents
- research assistants
- customer support systems

---

# Real Example

Imagine a **travel planning assistant**.

```
User
 │
 ▼
Travel Planner Agent
 │
 ├── Flight Agent
 ├── Hotel Agent
 └── Weather Agent
```

Each agent handles a specific domain.

---

# Key Takeaway

Multi-agent systems usually follow one of two patterns:

| Pattern | Best For |
| --- | --- |
| Sequential pipeline | linear workflows |
| Coordinator pattern | complex decision making |

The **coordinator pattern** is the most common in real systems.

---

# This Repository's Example

See [Section 10 — This Repository's Example](10-project-example.md) for the concrete coordinator + math + prime architecture in this repo.

---

# Transition to Advanced Topics

Now that we understand **how agents collaborate**, the next step is to explore **advanced capabilities of A2A systems**, including:

- streaming responses
- multi-turn interactions
- security and authentication
- observability and tracing

These features are important for **production agent systems**.

---

[← Previous: Section 8](08-a2a-client.md) | [Next: Section 10 — This Repository's Example →](10-project-example.md) | [Index](index.md)
