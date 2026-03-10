"""
Remote Math Agent — A2A Server (exposed via to_a2a)

This module implements a simple math agent that answers arithmetic questions.
It is exposed as an A2A-compatible service using to_a2a().

HOW IT WORKS:
  1. We create a standard ADK Agent with an LLM (Azure or Gemini)
  2. to_a2a() wraps it as a FastAPI app that speaks the A2A protocol
  3. The agent card (metadata) is auto-generated at /.well-known/agent-card.json
  4. Other agents can discover and call this agent over HTTP

RUN:
    uvicorn remote_math_agent:a2a_app --host 127.0.0.1 --port 8001

REQUIRES:
    - .env with LLM credentials (see .env.example)
    - Remote agents (math, prime) must be running before coordinator starts
"""

from dotenv import load_dotenv

load_dotenv()

from llm_config import get_llm_model
from google.adk.agents.llm_agent import Agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a

# LLM is selected by LLM_PROVIDER in .env (azure or gemini)
_model = get_llm_model()

# Standard ADK agent: name, model, and instruction define its behavior
root_agent = Agent(
    name="math_agent",
    model=_model,
    instruction=(
        "You are a remote math agent. "
        "Answer simple arithmetic questions clearly and briefly."
    ),
)

# to_a2a() converts our agent into an A2A-compatible ASGI app.
# - Creates routes for the A2A protocol (task submission, etc.)
# - Auto-generates agent card (skills, capabilities, URL)
# - port=8001 is used when building the agent card URL
a2a_app = to_a2a(root_agent, port=8001)
