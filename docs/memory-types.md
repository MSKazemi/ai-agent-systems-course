# Memory Types in Agentic Systems

Agentic systems don't just "store context" — they rely on **multiple memory types**, each serving a different role in reasoning, continuity, and learning.

This document maps every memory type to **concrete code** from the code executor agents in this repo (`code-executorv01`, `code-executorv02`).

---

## The Five Memory Types

| # | Type | Time Scope | Storage | Role |
|---|------|-----------|---------|------|
| 1 | **Short-term** | One run | LangGraph state / REPL locals | Intermediate reasoning |
| 2 | **Episodic** | Session(s) | Conversation list + pruning | Multi-turn continuity |
| 3 | **Semantic** | Long-term | System prompt injection | Domain knowledge |
| 4 | **Procedural** | Persistent | Tools + graph routing | How to act |
| 5 | **Reflective** | Growing | Execution logs | Learning from outcomes |

---

## 1. Short-Term Memory (Working / Context Memory)

**Definition:** Temporary state used within a single reasoning loop — fits inside the LLM's context window and is lost when the graph finishes.

**Purpose:**
- Pass intermediate results (code output, error messages) between graph nodes
- Track loop counters (`attempts`, `finalize_retries`) so the agent knows when to give up
- Hold the current dataset context

### In the Code Executor

The state object that flows through every graph node is defined in `code-executorv01/code_agent/graph.py`:

```python
class ExtendedState(TypedDict):
    messages: Annotated[list, add_messages]  # full conversation (append-only)
    data_context: str                        # dataset description
    attempts: int                            # how many LLM calls this turn
    finalize_retries: int                    # how many times finalize was retried
```

`add_messages` is LangGraph's built-in reducer — it **appends** new messages instead of replacing the list. This means every tool call result, every LLM reply, and every error message accumulates in `state["messages"]` as the agent loops:

```python
# agent_node — appends the LLM's tool call to state
def agent_node(state: ExtendedState, llm_wrapper) -> dict:
    attempts = state.get("attempts", 0) + 1
    response = llm_wrapper.invoke(state["messages"], allow_text=False)
    return {"messages": [response], "attempts": attempts}
    # LangGraph merges this into the running state via add_messages

# tools node — appends the execution result (stdout / error)
# finalize node — appends the plain-text answer
```

The Python REPL also acts as short-term memory: computed variables live in `_repl.locals` across tool calls within the same turn.

```python
# tools.py — shared, persistent REPL
_repl: PythonREPL = PythonREPL(_locals={})
```

When the agent generates code that creates `df_filtered`, that variable remains in `_repl.locals` for subsequent tool calls in the same session — the next code snippet can reference it without re-computing it.

**Key insight:** Short-term memory is ephemeral by design. The `clear` command in the interactive loop explicitly destroys it:

```python
# agent.py (v01)
if user_input.lower() == "clear":
    _repl.locals.clear()        # wipe REPL variables
    load_data(str(DEFAULT_DATA_FILE))  # reload fresh data
    conversation = [SystemMessage(content=full_prompt)]  # reset messages
```

---

## 2. Episodic Memory (Session / Multi-turn Memory)

**Definition:** Stores past interactions across multiple turns within (or across) sessions, enabling follow-up questions without re-stating context.

**Purpose:**
- "What's the peak power for rack A?" → "Now plot it" (second query knows which rack)
- Preserves the chain of reasoning across multiple user queries

### In the Code Executor

The `conversation` list in `agent.py` is the episodic memory. It grows with every turn:

```python
# agent.py (v01) — run_turn()
def run_turn(query, graph, data_context, conversation):
    user_msg = HumanMessage(content=f"**YOUR TASK:**\n{query}")
    input_messages = _prune(conversation + [user_msg])

    final_state = graph.invoke({"messages": input_messages, ...})
    new_messages = final_state["messages"][len(input_messages):]

    conversation.extend(new_messages)  # ← episodic memory grows here
    return answer, conversation
```

Because `conversation` is passed by reference and extended each turn, the agent "remembers" all prior exchanges without the user repeating themselves.

### Context Window Budget

Episodic memory is bounded by the LLM's context window. Both code executors enforce a sliding window:

```python
# agent.py (v01) — _prune()
def _prune(messages: list) -> list:
    if len(messages) <= MAX_MESSAGES:
        return messages
    return [messages[0]] + messages[-(MAX_MESSAGES - 1):]
    # always keep system prompt (index 0) + most recent N messages
```

```python
# agent.py (v02) — prune_conversation_history()
def prune_conversation_history(messages: list) -> list:
    if len(messages) <= MAX_MESSAGES:
        return messages
    system_prompt_msg = messages[0]
    recent = messages[-(MAX_MESSAGES - 1):]
    print(f"[CONTEXT] Pruned: {len(messages)} → {MAX_MESSAGES} messages", ...)
    return [system_prompt_msg] + recent
```

The pattern is the same: keep the system prompt fixed, slide the window over the rest.

### Cross-Session Episodic Memory

`code-executorv02` also persists REPL state to disk so variables survive a process restart:

```python
# config.py (v02)
REPL_STATE_PATH = STATE_DIR / "repl_state.pkl"
```

On the next startup, the agent can load `repl_state.pkl` to continue a session where it left off — this is episodic memory that survives process boundaries.

### Introspection for Context Injection

Before each query, `capture_repl_state_summary()` inspects the live REPL variables and injects a summary into the prompt:

```python
# agent.py (v02)
def capture_repl_state_summary() -> str:
    var_details = []
    for name, value in _repl.locals.items():
        if isinstance(value, pd.DataFrame):
            var_details.append(f"- **{name}** (DataFrame: {value.shape[0]} rows x ...)")
        elif isinstance(value, (int, float, str, bool)):
            var_details.append(f"- **{name}** = {repr(value)}")
        ...
    return "**REPL State - Available Variables:**\n" + "\n".join(var_details)
```

This summary is then prepended to the user's query:

```python
query_for_graph = (
    "**[CONTEXT]**\n"
    f"Current REPL state:\n{repl_state_summary}\n\n"
    "**[YOUR TASK]**\n"
    f"{original_query}"
)
```

The agent now knows that `df_hourly` already exists — it can reuse it instead of recomputing it. This is episodic memory made explicit.

---

## 3. Semantic Memory (Domain Knowledge)

**Definition:** Long-term knowledge about the problem domain — facts that don't change turn-to-turn. In RAG systems this lives in a vector store; here it is injected directly as structured text.

**Purpose:**
- Tell the model the shape and meaning of the dataset (column names, data ranges, time resolution)
- Ground code generation in real column names instead of hallucinated ones

### In the Code Executor

`format_data_context()` in `agent.py` builds the semantic context from CSV metadata:

```python
# agent.py (v01) — format_data_context()
def format_data_context(metadata: dict) -> str:
    ctx = f"**LOADED DATA:** DataFrame 'df' ({metadata['rows']} rows × {len(metadata['columns'])} columns)\n"

    ctx += "**COLUMNS:** " + ", ".join(metadata["columns"]) + "\n\n"

    ctx += "**NUMERIC COLUMNS (min, max, mean):**\n"
    for col, s in list(metadata["numeric_columns"].items())[:8]:
        ctx += f"- {col}: min={s['min']:.1f}, max={s['max']:.1f}, mean={s['mean']:.1f}\n"

    ctx += "**DATETIME COLUMNS:**\n"
    for col, info in metadata["datetime_columns"].items():
        ctx += f"- {col}: {info['min']} → {info['max']} (duration: {info['duration']})\n"

    return ctx
```

This context is appended to the system prompt once at startup and stays there for the whole session:

```python
full_prompt = f"{system_prompt}\n\n{data_context}"
conversation = [SystemMessage(content=full_prompt)]
```

**Why this counts as semantic memory:** The dataset description is static, external knowledge that informs every query. The model doesn't learn it from conversation — it's pre-loaded like a knowledge base.

`code-executorv02` also uses **few-shot examples** as semantic memory — concrete demonstrations of correct tool-call format baked into the conversation before the user's first message:

```python
# agent.py (v02)
if use_few_shot_examples:
    conversation.extend(get_few_shot_messages_for_mode())
```

`few_shot_examples.py` contains complete Human→AI→Tool→AI exchanges showing the model exactly what correct behavior looks like. This is domain knowledge about the tool protocol, not derived from user interaction.

---

## 4. Procedural Memory (Skills / Tool Logic)

**Definition:** Encodes *how to act* — the rules, tool schemas, and workflow structure that determine the agent's behavior. Set at agent-creation time and does not change during a session.

**Purpose:**
- Define which tools the agent can call and what arguments they take
- Enforce the ReAct loop protocol (WORK mode vs FINALIZE mode)
- Encode the routing logic that determines what happens after each action

### In the Code Executor — System Prompt

`system_prompt.py` is pure procedural memory: it tells the agent the rules of operation, not facts about the data.

```python
# system_prompt.py (v02) — TOOL_CALL_DISCIPLINE_NATIVE
TOOL_CALL_DISCIPLINE_NATIVE = """
- WORK LOOP (allow_text=False): you MUST call exactly one tool per turn.
- When correcting after an error marker, output the tool call only.
- FINALIZE (allow_text=True): you MUST output the final plain-text answer only (no tool call).
"""
```

This is analogous to a surgeon's checklist — it doesn't describe the patient (semantic memory), it encodes the *procedure*.

### In the Code Executor — Tool Schema

The `execute_python` tool definition in `tools.py` is procedural memory about what the agent can *do*:

```python
# tools.py (v02)
@tool
def execute_python(code: str) -> str:
    """
    Execute Python code in a persistent REPL environment.
    'df' is pre-loaded. Use matplotlib to save plots to plots/.
    Returns stdout + stderr. On error, returns [PYTHON_EXECUTION_FAILED].
    """
    ...
```

The docstring is parsed by the LLM as instructions for *how* to use the tool. It is procedural knowledge.

### In the Code Executor — Graph Routing

The `route_from_agent` and `route_from_tools` functions in `graph.py` are the procedural backbone of the agent — they encode the decision rules:

```python
# graph.py
def route_from_agent(state: ExtendedState) -> Route:
    last = state["messages"][-1]
    tool_calls = getattr(last, "tool_calls", []) or []
    latest_tool = _latest_tool_message(state)

    if state.get("attempts", 0) >= MAX_ITERATIONS:
        return Route.END               # give up after too many tries

    if _is_protocol_error(last):
        return Route.AGENT             # LLM produced bad output → retry

    if tool_calls:
        return Route.TOOLS             # good tool call → execute it

    if _tool_failed(latest_tool):
        return Route.AGENT             # execution failed → try to fix

    return Route.AGENT                 # no tool call → force one


def route_from_tools(state: ExtendedState) -> Route:
    latest_tool = _latest_tool_message(state)
    if _tool_failed(latest_tool):
        return Route.AGENT             # error → back to LLM for correction
    if _tool_succeeded(latest_tool):
        return Route.FINALIZE          # success → write the answer
    return Route.AGENT
```

This graph structure is procedural memory crystallised into code. It does not change per query — it is the fixed skill of the agent.

---

## 5. Reflective Memory (Learning / Experience)

**Definition:** Stores outcomes of past executions to surface patterns, enable post-hoc analysis, and support improvement over time.

**Purpose:**
- Audit which queries succeed and which fail
- Track correction flow (how many retries, what errors occurred)
- Enable human review and quality scoring
- Provide a dataset for future fine-tuning or prompt engineering

### In the Code Executor

`code-executorv02` has a dedicated logging system (`logger.py`) that records every execution as a structured JSONL entry:

```python
# logger.py (v02)
@dataclass
class ExecutionLog:
    query: str = ""
    completed: bool = False
    failure_reason: Optional[str] = None
    duration_seconds: float = 0.0
    correction_flow: List[Dict] = field(default_factory=list)  # retries + errors
    final_code: str = ""
    plots_generated: List[Dict] = field(default_factory=list)
    final_response: str = ""
    # Human evaluation fields (filled in post-run)
    human_eval_code_quality: Optional[int] = None    # 1..5
    human_eval_plot_quality: Optional[int] = None
    human_eval_response_quality: Optional[int] = None
    human_eval_tags: List[str] = field(default_factory=list)
```

The `correction_flow` field is particularly important — it records each retry: what went wrong, how many attempts it took, and whether recovery succeeded. Over many runs this becomes a corpus of failure patterns.

The logger is called at the start and end of every query execution:

```python
# agent.py (v02) — run_single_turn()
log_session = logger.start_logging(query=original_query)

# ... graph executes ...

log_session.set_final_code(final_code)
log_session.set_final_response(final_message_content)
log_session.finalize(attempts=attempts)
```

Logs are written to `logs/run_YYYYMMDD_HHMMSS.jsonl`. Over time this directory becomes reflective memory — a record of what worked and what didn't, queryable by pattern.

**How this enables improvement:** If `correction_flow` shows that a particular error (e.g., `KeyError: 'timestamp'`) always requires exactly one retry, you can encode a fix directly in the system prompt or few-shot examples — turning reflective memory into semantic or procedural memory.

---

## How All Five Types Work Together

Here is the full flow for a single query in `code-executorv02`:

```text
User: "Plot average CPU load per rack for the past week"
        │
        ▼
[Procedural]  system_prompt.py + graph routing rules determine how to proceed
[Semantic]    data_context (columns, time range, stats) grounds code generation
[Episodic]    conversation history tells the agent what was discussed before
        │
        ▼
  LangGraph: agent → tools → agent → tools → finalize
        │
  [Short-term] ExtendedState flows through nodes:
               messages, attempts, finalize_retries
               _repl.locals accumulates computed variables
        │
        ▼
[Reflective]  AgentLogger writes to logs/run_*.jsonl:
              query, final_code, correction_flow, duration, plots_generated
```

---

## Practical Mapping

| Memory Type | Implementation | File |
|-------------|---------------|------|
| Short-term | `ExtendedState` (graph state) + `_repl.locals` | `graph.py`, `tools.py` |
| Episodic | `conversation: list` + `_prune()` / `prune_conversation_history()` | `agent.py` |
| Episodic (cross-session) | `repl_state.pkl` serialization | `tools.py`, `config.py` (v02) |
| Semantic | `format_data_context()` + few-shot examples in system prompt | `agent.py`, `few_shot_examples.py` |
| Procedural | `system_prompt.py` rules + tool schemas + graph routing functions | `system_prompt.py`, `tools.py`, `graph.py` |
| Reflective | `AgentLogger` → `logs/run_*.jsonl` with correction_flow + human_eval | `logger.py` (v02) |

---

## Common Mistakes

### Mixing everything into short-term memory

If every fact — column names, past sessions, domain knowledge, execution history — is jammed into the conversation list, you get:
- Token explosion (context window overflow)
- Pruning that discards critical early context
- Confused reasoning when old and new facts collide

The code executor avoids this by giving each memory type its own home: dataset facts go in `data_context`, session facts go in `conversation`, execution history goes in `logs/`.

### No episodic memory (stateless chatbot)

If the conversation list is reset after every query, the agent cannot handle:
> "Now do the same but for rack B"

This is why `run_turn()` passes `conversation` by reference and accumulates messages across turns. The agent is stateful by design.

### Ignoring reflective memory

Without logging, you cannot answer: "Why does this agent fail on time-series queries?" The `correction_flow` field in `ExecutionLog` makes failure patterns visible and actionable.

---

## Further Reading

- `code-executorv01/code_agent/graph.py` — LangGraph state + routing
- `code-executorv01/code_agent/agent.py` — episodic memory (conversation + pruning)
- `code-executorv02/code_agent/agent.py` — REPL state introspection + logging
- `code-executorv02/code_agent/logger.py` — reflective memory schema
- `LangGraph/docs/02-what-is-langgraph.md` — LangGraph state fundamentals
