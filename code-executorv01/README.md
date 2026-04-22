# Code Execution Agent

A LangGraph-based AI agent that writes, runs, and self-corrects Python code in response to natural-language questions about a dataset.

This module teaches the **ReAct pattern** — the most common pattern for building AI agents. The model loops between *reasoning* (generating code) and *acting* (running it) until the task is solved.

---

## Quick Start

Make sure the SSH tunnel to the lab Ollama server is open (your instructor provides the credentials — see [lab-ollama-setup.md](../docs/lab-ollama-setup.md)).

Then run the agent:

```bash
cd code-executorv01/code_agent
python agent.py
```

Type a question and press Enter:

```
You: How many rows does the dataset have?
You: Plot average power consumption per rack as a bar chart
You: clear      ← resets conversation and REPL
You: quit       ← exits
```

---

## What It Does

You ask a natural-language question. The agent:

1. Generates Python code (pandas + matplotlib) to answer it
2. Runs the code in an isolated subprocess
3. If the code fails, reads the error and rewrites the code automatically
4. Once it succeeds, produces a plain-text summary — plots are saved to `plots/`

---

## The ReAct Pattern

ReAct (**Re**asoning + **Act**ing) is the loop at the heart of this agent:

```text
User question
     │
     ▼
  [agent] ──── LLM generates Python code (as a tool call)
     │
     ▼
  [tools] ──── Code runs in a subprocess
     │
     ├── FAILED ──► error fed back to [agent] → LLM fixes the code
     │
     └── SUCCESS ──► [finalize] ──── LLM writes a plain-text answer
                          │
                          ▼
                       Response to user
```

The loop runs up to `MAX_ITERATIONS` times (default 8). Each iteration is one LLM call.

---

## File Map

```text
code_agent/
├── agent.py         ← entry point: loads data, builds graph, runs the chat loop
├── graph.py         ← LangGraph state machine: nodes, routing, state
├── tools.py         ← execute_python tool: subprocess isolation, plot detection
├── llm_wrapper.py   ← Ollama calls + protocol enforcement
├── system_prompt.py ← system prompt injected at the start of every session
├── config.py        ← all config values (read from .env)
├── data/            ← CSV dataset loaded as 'df'
└── plots/           ← generated plots saved here as PNG
```

---

## How Each File Works

### `config.py` — Configuration

Reads all settings from the `.env` file using `python-dotenv`. Key values:

```python
OLLAMA_HOST   = "http://localhost:11434"   # Ollama via SSH tunnel
OLLAMA_MODEL  = "qwen3.5:35b"
TOOL_CALL_MODE = "native"                  # or "tagged" for older models
MAX_ITERATIONS = 8                         # max LLM calls per question
CODE_EXECUTION_TIMEOUT = 60               # seconds before subprocess is killed
```

---

### `tools.py` — The Tool

Defines the one tool the LLM can call: `execute_python(code: str)`.

**How it runs code safely:**

```text
execute_python(code)
  │
  ├── wrap code in try/except so tracebacks go to stdout
  │
  ├── spawn a fresh subprocess (forkserver/spawn — never inherits parent threads)
  │      ├── re-inject builtins: pd, np, plt, df, ...
  │      ├── reload df from CSV
  │      └── run the code, put result in a queue
  │
  └── parent reads the queue within CODE_EXECUTION_TIMEOUT seconds
         ├── timeout? → kill subprocess, return TimeoutError response
         └── result? → check output for errors or success
```

**Output the graph routes on:**

| Output contains | Meaning | Graph action |
| --- | --- | --- |
| `SUCCESS` | Code worked | → finalize |
| `[PYTHON_EXECUTION_FAILED]` | Runtime error | → back to agent |

**Plot enforcement** — if the code uses matplotlib:

- `plt.show()` → error: must save to file instead
- Plotting without `plt.savefig()` → error: must save the PNG
- Plots saved to `plots/` are detected automatically and included in the response

---

### `graph.py` — The State Machine

Defines the LangGraph graph with three nodes and routing between them.

**State** (`ExtendedState`) — flows through every node:

```python
class ExtendedState(TypedDict):
    messages: Annotated[list, add_messages]  # full conversation history
    data_context: str                         # dataset description
    attempts: int                             # LLM calls so far (agent only)
    finalize_retries: int                     # finalize retry counter
```

**Nodes:**

| Node | What it does | Increments `attempts`? |
| --- | --- | --- |
| `agent` | Calls the LLM — must produce a tool call | Yes |
| `tools` | Runs `execute_python` via LangGraph's `ToolNode` | No |
| `finalize` | One final LLM call — must produce plain text | No |

**Routing after `agent`:**

```text
protocol error (no tool call)  → retry agent
tool call present              → tools
attempts >= MAX_ITERATIONS     → end
```

**Routing after `tools`:**

```text
[PYTHON_EXECUTION_FAILED]  → back to agent (self-correction loop)
SUCCESS                    → finalize
attempts >= MAX_ITERATIONS → end
```

**Routing after `finalize`:**

```text
tool call in response (forbidden) → retry finalize (max 1 retry, then fallback)
plain text                        → end
```

---

### `llm_wrapper.py` — Protocol Enforcement

`OllamaEnforcingWrapper` wraps the `ChatOllama` model and enforces a strict contract on every response.

**Why enforcement is needed:**

Local models (7–35 B parameters) sometimes produce plain text instead of tool calls, or emit tool calls when only plain text is expected. Prompt engineering alone is not reliable enough. The wrapper catches violations programmatically and forces a retry.

**Work loop (`allow_text=False`):**

```text
LLM response
  ├── has tool call → SUCCESS, pass through
  ├── no tool call + unresolved error → inject enforcement message → graph retries
  └── no tool call → PROTOCOL_ERROR → graph retries agent node
```

**Finalize (`allow_text=True`):**

```text
LLM response
  ├── plain text → OK, pass through
  └── tool call → PROTOCOL_ERROR → graph retries finalize node
```

**Two tool-call modes** (set via `TOOL_CALL_MODE` in `.env`):

- `native` — uses Ollama's built-in function calling API. Works with `llama3.1`, `qwen2.5`, `qwen3.5`, etc.
- `tagged` — parses `<tool_call>{...}</tool_call>` XML tags from raw text. For models without native function calling.

---

### `agent.py` — Entry Point and Chat Loop

**Startup sequence (`main`):**

```text
1. load_data(device_data.csv)
      → reads CSV into REPL as 'df'
      → returns metadata (rows, columns, dtypes, datetime info)

2. format_data_context(metadata)
      → formats metadata into a string the LLM can read
      → injected into the system prompt

3. create_graph(tools, system_prompt)
      → builds and compiles the LangGraph graph

4. interactive_loop(graph, data_context)
      → runs the chat REPL
```

**Per-turn flow (`run_turn`):**

```text
user query
  → wrapped in HumanMessage
  → pruned conversation (keeps system prompt + last MAX_MESSAGES messages)
  → graph.invoke(initial_state)
  → extract final answer from new messages
  → return answer + updated conversation
```

**Data context injected into every session:**

```text
- 5-row preview of the dataset
- Row and column count
- All column names
- Numeric stats (min, max, mean) for up to 8 numeric columns
- Datetime column ranges and sampling frequency
```

---

## Self-Correction in Action

```text
You: Plot CPU usage per rack

agent  → generates code with plt.show()
tools  → [PYTHON_EXECUTION_FAILED: PlotProtocolViolation — use plt.savefig() instead]
agent  → sees the error, regenerates code with plt.savefig()
tools  → SUCCESS — plot saved to plots/cpu_per_rack.png
finalize → "Here is the average CPU usage per rack. The highest is R03 at 87%..."
```

---

## Dataset

`data/device_data.csv` — mock HPC telemetry data. Loaded automatically at startup as the pandas DataFrame `df`. All generated code can use `df` directly without importing or loading it.

---

## Configuration (`.env`)

| Variable | Default | Description |
| --- | --- | --- |
| `OLLAMA_HOST` | `http://127.0.0.1:11434` | Ollama server URL |
| `OLLAMA_MODEL` | `llama3.1:8b` | Model to use |
| `TOOL_CALL_MODE` | `native` | `native` or `tagged` |
| `TEMPERATURE` | `0.1` | Sampling temperature — lower = more deterministic |
| `OLLAMA_NUM_CTX` | `32768` | Context window size in tokens |
| `MAX_TOKENS` | `8192` | Max tokens per LLM response |
| `MAX_ITERATIONS` | `8` | Max agent LLM calls per question |
| `CODE_EXECUTION_TIMEOUT` | `60` | Subprocess timeout in seconds |
| `MAX_MESSAGES` | `30` | Max conversation messages before pruning |
