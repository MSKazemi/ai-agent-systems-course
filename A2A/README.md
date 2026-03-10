# A2A (Agent-to-Agent) — Learning Example

A minimal example of Google ADK's A2A protocol: one agent delegates to another over HTTP. Uses **Azure OpenAI** or **Gemini** as the LLM.

---

## Teaching Materials

Structured course content on the A2A protocol is in the [`docs/`](docs/) folder:

| # | Topic |
|---|-------|
| 1 | [The Problem A2A Solves](docs/01-problem-a2a-solves.md) |
| 2 | [A2A Core Concepts](docs/02-a2a-core-concepts.md) |
| 3 | [A2A vs MCP vs APIs](docs/03-a2a-vs-mcp-vs-apis.md) |
| 4 | [A2A Architecture](docs/04-a2a-architecture.md) |
| 5 | [Environment Setup](docs/05-environment-setup.md) |
| 6 | [Build First Agent](docs/06-build-first-agent.md) |
| 7 | [Expose Agent with A2A](docs/07-expose-agent-a2a.md) |
| 8 | [A2A Client](docs/08-a2a-client.md) |
| 9 | [Agent Orchestration](docs/09-agent-orchestration.md) |

**[→ Full index](docs/index.md)**

---

## What is A2A?

**Agent-to-Agent (A2A)** lets agents call each other across processes. Instead of one large agent, you build smaller agents that specialize and delegate.

```
You → Coordinator → Remote Math Agent (port 8001)
      (port 8002) → Remote Prime Agent (port 8003)
```

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

---

## Quick Start

### 1. Install

```bash
pip install -r requirements.txt
```

### 2. Configure

```bash
cp .env.example .env
```

Edit `.env`. For **Azure OpenAI**:

```
LLM_PROVIDER=azure
AZURE_OPENAI_API_KEY=<from Azure Portal → Keys and Endpoint>
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-08-01-preview
AZURE_PRIMARY_LLM_DEPLOYMENT_NAME=gpt-4o
```

For **Gemini**:

```
LLM_PROVIDER=gemini
GOOGLE_API_KEY=<from aistudio.google.com/apikey>
```

### 3. Run

**Terminal 1 — Math agent (port 8001):**

```bash
uvicorn remote_math_agent:a2a_app --host 127.0.0.1 --port 8001
```

**Terminal 2 — Prime agent (port 8003):**

```bash
uvicorn remote_prime_agent:a2a_app --host 127.0.0.1 --port 8003
```

**Terminal 3 — Coordinator (chat UI):**

```bash
adk web . --port 8002
```

Open http://127.0.0.1:8002. Select **coordinator** (static) or **dynamic_coordinator** (registry-based), and try:

- *"What is 17 + 23?"* → delegates to math agent
- *"Is 17 a prime number?"* → delegates to prime agent

---

## Project Structure

```
A2A/
├── remote_math_agent.py      # Math agent (port 8001)
├── remote_prime_agent.py     # Prime agent (port 8003)
├── coordinator_agent.py     # Static coordinator (hardcoded agents)
├── dynamic_coordinator_agent.py   # Dynamic coordinator (registry-based)
├── agent_registry.json       # Registry of available agents
├── registry_server.py        # Optional: HTTP registry (port 8004)
├── coordinator/              # ADK discovery (static)
├── dynamic_coordinator/      # ADK discovery (dynamic)
├── docs/                     # Teaching materials (9 sections)
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

## A2A Patterns

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

## Verify Azure

If you get 401 errors, test your credentials:

```bash
python verify_azure.py
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No agents found | Run `adk web` from project root |
| Port in use | Use `adk web . --port 8003` |
| Azure 401 | Regenerate key in Azure Portal, update `.env` |
| Remote unreachable | Start both uvicorn servers (8001, 8003) before adk web |

---

## Links

- [ADK A2A docs](https://google.github.io/adk-docs/a2a/intro/)
- [A2A protocol](https://a2a.protocol.org/)
