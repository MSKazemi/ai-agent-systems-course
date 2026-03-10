# This Repository's Example

This section describes the **concrete implementation** in this repo: a coordinator that delegates to math and prime agents.

---

## Architecture

```
┌─────────────────────────────┐
│  Coordinator                │
│  adk web :8002              │
└──────────┬──────────────────┘
           │ A2A (HTTP)
     ┌─────┴─────┐
     ▼           ▼
┌─────────────┐  ┌─────────────┐
│ Math Agent  │  │ Prime Agent │
│ uvicorn 8001│  │ uvicorn 8003│
│ arithmetic  │  │ is N prime? │
└─────────────┘  └─────────────┘
```

The coordinator runs on port 8002 and delegates to:
- **Math Agent** (port 8001) — arithmetic
- **Prime Agent** (port 8003) — primality checks

---

## Project Structure

```
A2A/
├── remote_math_agent.py      # Math agent (port 8001)
├── remote_prime_agent.py     # Prime agent (port 8003)
├── coordinator_agent.py      # Static coordinator (hardcoded agents)
├── dynamic_coordinator_agent.py   # Dynamic coordinator (registry-based)
├── agent_registry.json       # Registry of available agents
├── registry_server.py        # Optional: HTTP registry (port 8004)
├── coordinator/              # ADK discovery (static)
├── dynamic_coordinator/      # ADK discovery (dynamic)
├── docs/                     # Teaching materials
├── llm_config.py
├── verify_azure.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## Static vs Dynamic Orchestration

| Pattern | When agents are known | Example |
|--------|------------------------|---------|
| **Static** | Development time (hardcoded) | `coordinator` |
| **Dynamic** | Runtime (from registry) | `dynamic_coordinator` |

### Static (simple)

Agents are hardcoded in `coordinator_agent.py`:

```python
math_remote = RemoteA2aAgent(name="remote_math", agent_card="http://...")
root_agent = Agent(sub_agents=[math_remote])
```

### Dynamic (scalable)

Agents are discovered from a registry at runtime:

```python
# agent_registry.json
{"agents": [{"name": "remote_math", "agent_card": "http://127.0.0.1:8001/..."}]}

# dynamic_coordinator_agent.py
sub_agents = load_agents_from_registry()  # from file or REGISTRY_URL
root_agent = Agent(sub_agents=sub_agents)
```

**Run the dynamic coordinator:** Same as static — select `dynamic_coordinator` in the UI. It reads `agent_registry.json` at startup. To add a new agent, edit the registry; no code change.

**Optional HTTP registry:**

```bash
uvicorn registry_server:app --host 127.0.0.1 --port 8004
```

Add `REGISTRY_URL=http://127.0.0.1:8004/agents` to `.env` — the dynamic coordinator will fetch from the registry API instead of the file.

---

## A2A Patterns in This Repo

### Expose an agent

Use `to_a2a()` to serve an agent over HTTP:

```python
from google.adk.agents.llm_agent import Agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a

agent = Agent(name="math_agent", model="...", instruction="...")
a2a_app = to_a2a(agent, port=8001)
# Run: uvicorn module:a2a_app --port 8001
```

### Consume a remote agent

Use `RemoteA2aAgent` to call another agent as a sub-agent:

```python
from google.adk.agents.llm_agent import Agent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent, AGENT_CARD_WELL_KNOWN_PATH

remote = RemoteA2aAgent(
    name="remote_math",
    description="Does arithmetic",
    agent_card=f"http://127.0.0.1:8001{AGENT_CARD_WELL_KNOWN_PATH}",
)

coordinator = Agent(
    name="coordinator",
    model="...",
    instruction="Delegate math to remote_math.",
    sub_agents=[remote],
)
```

---

## Agent Card

Each A2A agent exposes an agent card at `/.well-known/agent-card.json`:

```bash
curl http://127.0.0.1:8001/.well-known/agent-card.json
```

Remote agents discover each other via this URL.

---

[← Previous: Section 9](09-agent-orchestration.md) | [Index](index.md)
