# Section 6 — Build First Agent (Hands-on)

In this section, students build their **first real ADK agent**.

The goal is not A2A yet.

The goal is to understand:

- what an ADK agent file looks like
- what `root_agent` means
- how to run the agent
- how to test it in the browser

This gives students a solid base before exposing the agent through **A2A** later. ([Google GitHub](https://google.github.io/adk-docs/get-started/python/))

---

## What students learn here

By the end of this section, students should understand:

- an ADK project contains an `agent.py` file and a `root_agent`
- an ADK agent can have a **name**, **description**, **instruction**, **model**, and optional **tools**
- `adk run` is useful for terminal testing
- `adk web` is useful for browser-based testing. ([Google GitHub](https://google.github.io/adk-docs/get-started/python/))

---

## Minimal project structure

Use a very small project first:

```
my_agent/
├── agent.py
├── __init__.py
└── .env
```

ADK's Python quickstart uses this same idea: a folder containing `agent.py`, `.env`, and `__init__.py`, with `root_agent` defined in `agent.py`. ([Google GitHub](https://google.github.io/adk-docs/get-started/python/))

---

## `__init__.py`

```python
from . import agent
```

This helps ADK recognize the agent package in the project structure shown in the docs. ([Google GitHub](https://google.github.io/adk-docs/get-started/quickstart/))

---

## First simple agent

For teaching, start with a **single-tool agent**.

That is better than an "empty echo" example because students immediately see:

- the agent has reasoning
- the agent can call a function
- ADK connects the model to Python tools

### `agent.py`

```python
from google.adk.agents.llm_agent import Agent

def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    return {
        "status": "success",
        "city": city,
        "time": "10:30 AM"
    }

root_agent = Agent(
    model="gemini-3-flash-preview",
    name="time_agent",
    description="Tells the current time in a specified city.",
    instruction="You are a helpful assistant. Use the get_current_time tool when the user asks for time in a city.",
    tools=[get_current_time],
)
```

This structure matches the current ADK Python quickstart pattern: import `Agent`, define a tool function, and assign an `Agent(...)` instance to `root_agent`. ([Google GitHub](https://google.github.io/adk-docs/get-started/python/))

---

## `.env`

Students also need to set the API key in `.env`:

```bash
GOOGLE_API_KEY="YOUR_API_KEY"
```

The ADK Python quickstart uses `GOOGLE_API_KEY` in `.env` for Gemini API access. ([Google GitHub](https://google.github.io/adk-docs/get-started/python/))

---

## Run in terminal

From the **parent directory** that contains `my_agent/`, run:

```bash
adk run my_agent
```

This launches the interactive CLI for the agent. ([Google GitHub](https://google.github.io/adk-docs/get-started/python/))

Example prompt:

```
What time is it in Rome?
```

---

## Run in browser

To open the development web UI:

```bash
adk web --port 8000
```

Then open:

```
http://localhost:8000
```

In the web UI, students select the agent and test it interactively. Google's quickstart describes `adk web` as the browser interface for testing and debugging, and notes it is for development use. ([Google GitHub](https://google.github.io/adk-docs/get-started/python/))

---

## Why this example is good for teaching

This first agent is good because it is:

- small
- easy to read
- real ADK code
- enough to explain `tool`, `instruction`, and `root_agent`

It also avoids too much complexity too early.

---

## What to explain line by line

### `from google.adk.agents.llm_agent import Agent`

This imports the ADK agent class used in the Python quickstart. ([Google GitHub](https://google.github.io/adk-docs/get-started/python/))

### `def get_current_time(...)`

This is a normal Python function. ADK can expose Python functions as tools, and the docs explain that ADK inspects function signatures, descriptions, and parameters to generate tool schemas for the model. ([Google ADK documentation](https://google.github.io/adk-docs/tools-custom/function-tools/))

### `root_agent = Agent(...)`

This is the main object ADK looks for in the project. The quickstart states that `root_agent` is the only required element of an ADK agent project. ([Google GitHub](https://google.github.io/adk-docs/get-started/python/))

### `instruction=...`

This tells the model how to behave.

### `tools=[get_current_time]`

This makes the function available as a tool the agent can use.

---

## Suggested live demo flow

A simple teaching sequence:

1. Show the folder structure.
2. Paste the code.
3. Add the API key to `.env`.
4. Run `adk run my_agent`.
5. Ask: "What time is it in Paris?"
6. Then open `adk web --port 8000`.
7. Test the same prompt in the browser.

This gives students a full "I built an agent and it works" moment very early.

---

## Teaching note

For **Section 6**, A2A should **not** be introduced yet.

First let students understand:

- an agent exists
- it has a tool
- it can run locally
- ADK provides a dev interface

Then in the next section you can say:

> "Now we already have a working ADK agent. Let's expose it to other agents using A2A."
> 

That transition is very natural.

---

## Section 6 summary

### Section 6 — Build Your First ADK Agent (Hands-on)

- create a minimal ADK agent project
- define a `root_agent`
- add one simple Python tool
- run the agent in the terminal with `adk run`
- test the agent in the browser with `adk web`

**Learning outcome:**

Students can build and test a real ADK agent locally before exposing it through A2A. ([Google GitHub](https://google.github.io/adk-docs/get-started/python/))

---

## Recommended first prompt examples

Use very simple prompts:

- "What time is it in Rome?"
- "Tell me the time in Bologna."
- "What is the current time in Tehran?"

These keep the focus on the ADK flow rather than complex reasoning.

---

[← Previous: Section 5](05-environment-setup.md) | [Next: Section 7 — Expose Agent with A2A →](07-expose-agent-a2a.md)
