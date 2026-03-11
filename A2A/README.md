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
| 10 | [This Repository's Example](docs/10-project-example.md) |

**[→ Full index](docs/index.md)**

---

## Get the Repository

```bash
git clone git@github.com:MSKazemi/ai-agent-systems-course.git
cd ai-agent-systems-course/A2A
```

Or with HTTPS:

```bash
git clone https://github.com/MSKazemi/ai-agent-systems-course.git
cd ai-agent-systems-course/A2A
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

Open http://127.0.0.1:8002. Select **coordinator** or **dynamic_coordinator**, and try:

- *"What is 17 + 23?"* → delegates to math agent
- *"Is 17 a prime number?"* → delegates to prime agent

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
