# A2A (Agent-to-Agent) — Learning Module

Learn how agents communicate with and delegate to other agents over HTTP. One coordinator receives a user request and routes it to the right specialist agent — a math agent, a prime-checking agent, or any other agent registered in the system.

**Prerequisite:** Complete the [MCP module](../MCP/README.md) first. It explains how LLMs call tools, which is the foundation for how agents work here.

---

## What You'll Learn

- Why agents need to delegate to other agents (and when one agent isn't enough)
- How A2A lets agents discover each other and communicate over HTTP
- How to expose a Python agent as an HTTP service with `to_a2a()`
- How a coordinator routes user requests to the right specialist
- The difference between static orchestration (hardcoded agents) and dynamic orchestration (registry-based)

---

## Teaching Docs — Read These First

Work through the docs in order before running any code. Each doc is short and builds on the previous one.


| #   | Topic                                                                                        |
| --- | -------------------------------------------------------------------------------------------- |
| 1   | [The Problem A2A Solves](docs/01-problem-a2a-solves.md) — why one agent isn't enough         |
| 2   | [A2A Core Concepts](docs/02-a2a-core-concepts.md) — agents, agent cards, skills, tasks       |
| 3   | [A2A vs MCP vs APIs](docs/03-a2a-vs-mcp-vs-apis.md) — when to use which                      |
| 4   | [A2A Architecture](docs/04-a2a-architecture.md) — how the protocol works                     |
| 5   | [Environment Setup](docs/05-environment-setup.md) — API keys and configuration               |
| 6   | [Build Your First Agent](docs/06-build-first-agent.md) — create an ADK agent from scratch    |
| 7   | [Expose an Agent with A2A](docs/07-expose-agent-a2a.md) — turn an agent into an HTTP service |
| 8   | [A2A Client](docs/08-a2a-client.md) — connect to a remote agent                              |
| 9   | [Agent Orchestration](docs/09-agent-orchestration.md) — static vs dynamic coordination       |
| 10  | [This Repository's Example](docs/10-project-example.md) — how all the pieces fit together    |


---

## What This Example Runs

When you follow the Quick Start below, you will have three services running:

```text
User
  └─▶ Coordinator (adk web, port 8002)
        ├─▶ Math Agent    (port 8001) — handles arithmetic
        └─▶ Prime Agent   (port 8003) — checks if numbers are prime
```

The coordinator receives your question, decides which specialist to call, delegates the work, and returns the answer. You never call the math or prime agents directly.

For dynamic orchestration, a registry server (port 8004) also runs and the coordinator discovers agents from it at startup instead of having their URLs hardcoded.

---

## Quick Start

### 1. Install

```bash
cd ai-agent-systems-course/A2A
python3 -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

### 2. Configure

```bash
cp .env.example .env
```

Edit `.env` with your LLM provider credentials.

**Azure OpenAI:**

```env
LLM_PROVIDER=azure
AZURE_OPENAI_API_KEY=<from Azure Portal → Keys and Endpoint>
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-08-01-preview
AZURE_PRIMARY_LLM_DEPLOYMENT_NAME=gpt-4o
```

**Google Gemini (free tier available):**

```env
LLM_PROVIDER=gemini
GOOGLE_API_KEY=<from aistudio.google.com/apikey>
```

**Ollama (local, no API key needed):**

```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.2
OLLAMA_BASE_URL=http://localhost:11434
```

### 3. Run (static coordinator)

Open four terminals, all with the virtual environment activated (`source .venv/bin/activate`).

**Terminal 1 — Math agent:**

```bash
uvicorn remote_math_agent:a2a_app --host 127.0.0.1 --port 8001
```

**Terminal 2 — Prime agent:**

```bash
d 
```

**Terminal 3 — Coordinator (chat UI):**

```bash
adk web . --port 8002
```

Open [http://127.0.0.1:8002](http://127.0.0.1:8002), select **coordinator**, and try:

- *"What is 17 + 23?"* → delegates to math agent
- *"Is 17 a prime number?"* → delegates to prime agent
- *"What is 144 + 56, and is the result prime?"* → uses both agents

### 4. Run (dynamic coordinator with registry)

Same as above, but also start the registry server, and select **dynamic_coordinator** in the UI.

**Terminal 4 — Registry server:**

```bash
uvicorn registry_server:app --host 127.0.0.1 --port 8004
```

The dynamic coordinator reads agent URLs from the registry at startup instead of having them hardcoded. See [agent_registry.json](agent_registry.json) to understand the registry format.

---

## Troubleshooting


| Problem                  | Solution                                                                                                                             |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| No agents found in UI    | Run `adk web` from the `A2A/` directory, not the repo root                                                                           |
| Port already in use      | Change port: `uvicorn remote_math_agent:a2a_app --port 8011`                                                                         |
| Azure 401 error          | Regenerate key in Azure Portal, update `.env`, run `python verify_azure.py`                                                          |
| Remote agent unreachable | Start both uvicorn servers (8001, 8003) **before** running `adk web`                                                                 |
| `pip: cannot execute`    | Recreate venv: `deactivate && rm -rf .venv && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt` |


---

## Key Files


| File                           | What it does                                                   |
| ------------------------------ | -------------------------------------------------------------- |
| `remote_math_agent.py`         | Math specialist — handles arithmetic, runs on port 8001        |
| `remote_prime_agent.py`        | Prime checker — checks if numbers are prime, runs on port 8003 |
| `coordinator_agent.py`         | Static coordinator — agent URLs hardcoded                      |
| `dynamic_coordinator_agent.py` | Dynamic coordinator — loads agents from registry at startup    |
| `registry_server.py`           | HTTP registry listing available agents, runs on port 8004      |
| `agent_registry.json`          | Registry config file — add agents here for dynamic discovery   |
| `llm_config.py`                | LLM provider abstraction — supports Azure, Gemini, Ollama      |


---

## Links

- [Google ADK A2A docs](https://google.github.io/adk-docs/a2a/intro/)
- [A2A protocol specification](https://a2a.protocol.org/)

