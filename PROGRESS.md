# Course Development Progress

## Completed

- [x] **MCP module** — docs (6), examples (4), exercises (3), solutions
- [x] **A2A module** — docs (10), coordinator, dynamic coordinator, registry server, remote agents
- [x] **DeepAgent module** — docs (4), examples (3: hello, custom tools, subagents)
- [x] **LangGraph primer module** — docs (3), examples (2: chain+tools, ReAct graph)
- [x] **Unified LLM config** — root `.env.example`, root `llm_config.py`; all modules default to Ollama; standardized env var names
- [x] **Single venv** — root `requirements.txt` covering all modules; per-module `requirements.txt` kept for standalone use
- [x] **Git pull guide** — cross-platform (Linux/Mac/Windows) instructions in root README
- [x] **Ollama support** — MCP (Mohsen), A2A (Andrea), DeepAgent updated, LangGraph examples use Ollama by default
- [x] **find_dotenv()** — all `llm_config.py` files walk upward to find root `.env`

## In Progress

- [ ] **LangGraph exercises** — hands-on tasks for the primer module
- [ ] **DeepAgent exercises** — hands-on tasks for Module 3

## Backlog

- [ ] **LangGraph docs** — additional docs on memory, persistence, streaming
- [ ] **MCP .env.example** — add a formal `.env.example` to the MCP module
- [ ] **A2A verify_azure.py** — update to also verify Ollama connectivity
- [ ] **Course intro video** — overview walkthrough for new students
- [ ] **Windows Ollama setup guide** — add to MCP Windows doc
