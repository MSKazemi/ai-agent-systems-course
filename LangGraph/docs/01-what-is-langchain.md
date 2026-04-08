# 01 — What is LangChain?

LangChain is a framework for building applications with LLMs. It gives you:

- A **standard interface** for chat models (same code works with OpenAI, Gemini, Ollama, …)
- **Tool calling** built in — define a Python function, the LLM can call it
- **LCEL** (LangChain Expression Language) — chain steps together with `|`

---

## The core interface: ChatModel

Every LangChain model takes a list of **messages** and returns a message.

```python
from langchain_ollama import ChatOllama

model = ChatOllama(model="qwen3.5:35b", base_url="http://localhost:11434")

from langchain_core.messages import HumanMessage

response = model.invoke([HumanMessage(content="What is 2 + 2?")])
print(response.content)   # "4"
```

Three message types you'll see everywhere:

| Type | Meaning |
|------|---------|
| `HumanMessage` | User's input |
| `AIMessage` | Model's response |
| `ToolMessage` | Result of a tool call |

---

## Tools

A **tool** is a Python function the LLM can call. Decorate it with `@tool`:

```python
from langchain_core.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b
```

The docstring becomes the tool description the LLM reads. Keep it clear.

Bind tools to a model so the LLM knows they exist:

```python
model_with_tools = model.bind_tools([multiply])
```

When the LLM wants to call a tool, its response contains a `tool_calls` list instead of text.

---

## LCEL: chaining with `|`

LCEL lets you pipe steps together. A minimal chain:

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{question}"),
])

chain = prompt | model

result = chain.invoke({"question": "What is the capital of France?"})
print(result.content)   # "Paris"
```

`chain.invoke(input)` runs every step left to right, passing the output of each step as input to the next.

---

## Key takeaway

LangChain gives you a uniform way to talk to any LLM, define tools it can call, and chain steps together. LangGraph (next doc) builds on this to create **stateful loops** — which is what agents need.
