# Section 5 — Environment Setup (Hands-on)

In this section we will prepare the development environment to **build and run A2A agents**.

Several implementations of the A2A protocol exist.

However, some are easier than others for **learning and teaching**.

---

# Available Implementations

| Implementation | Description | Difficulty |
| --- | --- | --- |
| **Google ADK** | Agent Development Kit with built-in A2A support | ⭐ Easy |
| **Python A2A SDK** | Reference implementation of the protocol | Medium |
| **LangGraph Integration** | A2A agents integrated with LangGraph workflows | Advanced |

---

# Why We Use Google ADK

For this course we will use **Google ADK (Agent Development Kit)**.

It is ideal for learning because it provides:

| Feature | Benefit |
| --- | --- |
| Built-in agent runtime | no need to build infrastructure |
| A2A server | expose agents easily |
| Dev UI | interact with agents in the browser |
| Simple Python API | easy to learn |

Using ADK allows us to **focus on A2A concepts instead of infrastructure**.

---

# System Requirements

Students should have:

- Python **3.10+**
- pip
- internet connection

Check Python version:

```
python --version
```

Example output:

```
Python 3.11.6
```

---

# Create a Virtual Environment (Recommended)

Using a virtual environment keeps dependencies isolated.

### Create environment

```
python -m venv .venv
```

### Activate (Linux / Mac)

```
source .venv/bin/activate
```

### Activate (Windows)

```
.venv\Scripts\activate
```

After activation you should see:

```
(.venv)
```

in your terminal.

---

# Install Google ADK

Install the package using pip:

```
pip install google-adk
```

Verify installation:

```
adk --help
```

You should see the CLI commands.

Example:

```
run
api_server
dev-ui
```

---

# ADK Project Structure

For this course we will use a simple project structure.

```
a2a-course
│
├── coordinator
│   └── agent.py
│
├── research_agent
│   └── agent.py
│
└── requirements.txt
```

Each folder represents **one agent**.

This allows us to build **multi-agent systems**.

---

# Running the Development UI

ADK provides a **Dev UI** for interacting with agents in the browser.

Run:

```
adk web --port 8000
```

Then open your browser:

```
http://localhost:8000
```

The UI allows you to:

- chat with the agent
- test prompts
- inspect sessions
- debug responses

---

# Running the A2A Server

Later in the course we will expose agents using the **A2A protocol**.

Run:

```
adk api_server --a2a
```

This starts a server that exposes endpoints like:

```
/agent.json
/tasks
/health
```

Other agents can now **discover and call this agent**.

---

# Quick Verification

Test the server in your browser:

```
http://localhost:8000/agent.json
```

You should see the **agent card**.

Example:

```json
{
  "name": "research-agent",
  "skills": ["search", "summarize"]
}
```

---

# What Students Should Achieve

By the end of this section students should be able to:

✅ install Google ADK

✅ run the development UI

✅ start an A2A server

✅ view an agent card

This prepares us for the next step: **building our first A2A agent**.

---

[← Previous: Section 4](04-a2a-architecture.md) | [Next: Section 6 — Build First Agent →](06-build-first-agent.md)
