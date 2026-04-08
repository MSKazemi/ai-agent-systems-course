# 02 — What is LangGraph?

LangGraph is a library for building **stateful, multi-step agent loops** using a graph of nodes and edges.

Where LangChain gives you a linear chain (A → B → C), LangGraph lets you add **loops** and **conditional branching** — exactly what an agent needs to keep calling tools until it's done.

---

## Four concepts

### 1. State

State is a typed dictionary that flows through the entire graph. Every node reads from it and writes back to it.

```python
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
```

`add_messages` is a special reducer: instead of replacing the list, it appends. So every node that adds a message accumulates the conversation history.

### 2. Nodes

A node is a Python function that takes state, does something, and returns a partial state update.

```python
def call_model(state: AgentState):
    response = model.invoke(state["messages"])
    return {"messages": [response]}   # appended, not replaced
```

### 3. Edges

Edges connect nodes. They can be:

- **Direct**: always go from A to B
- **Conditional**: branch based on state

```python
from langgraph.graph import END

def should_continue(state: AgentState):
    last = state["messages"][-1]
    if last.tool_calls:
        return "tools"   # → ToolNode
    return END           # → done
```

### 4. The graph

Wire it all together:

```python
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

builder = StateGraph(AgentState)

builder.add_node("agent", call_model)
builder.add_node("tools", ToolNode(tools))

builder.set_entry_point("agent")
builder.add_conditional_edges("agent", should_continue)
builder.add_edge("tools", "agent")   # after tools, back to agent

graph = builder.compile()
```

---

## Running the graph

```python
from langchain_core.messages import HumanMessage

result = graph.invoke({
    "messages": [HumanMessage(content="What is 6 * 7?")]
})

print(result["messages"][-1].content)   # "42"
```

`invoke` runs the graph until it reaches `END`, passing state through each node.

---

## Visual model

```
        ┌──────────────────────────┐
        │                          ▼
[START] → agent ── has tool calls? → tools
              └── no tool calls? → [END]
```

The agent keeps looping through `agent → tools → agent` until it has an answer.

---

## Key takeaway

LangGraph turns the agent loop into an explicit graph you can see, debug, and extend. The next doc shows exactly how this loop maps to the **ReAct pattern** that powers DeepAgent.
