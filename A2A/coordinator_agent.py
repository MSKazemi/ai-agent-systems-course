"""
Static Coordinator Agent — consumes remote agents via A2A

This is the SIMPLE (static) orchestration pattern: remote agents are
hardcoded. The coordinator knows exactly which agents exist at development time.

HOW IT WORKS:
  1. RemoteA2aAgent wraps a reference to another agent by its agent card URL
  2. agent_card = URL to /.well-known/agent-card.json on the remote server
  3. When the user asks a question, the coordinator's LLM decides which
     sub_agent to delegate to, then ADK calls that agent over HTTP (A2A)
  4. The remote agent processes the task and returns the result

ARCHITECTURE:
    User → Coordinator (this agent) → Remote Math (8001)
                                  → Remote Prime (8003)

RUN:
    Start remote agents first (8001, 8003), then:
    adk web . --port 8002
    Select "coordinator" in the UI.
"""

from dotenv import load_dotenv

load_dotenv()

from llm_config import get_llm_model
from google.adk.agents.llm_agent import Agent
from google.adk.agents.remote_a2a_agent import (
    RemoteA2aAgent,
    AGENT_CARD_WELL_KNOWN_PATH,
)

# AGENT_CARD_WELL_KNOWN_PATH = "/.well-known/agent-card.json"
# The standard path where A2A agents expose their metadata (skills, URL, etc.)

# --- Remote agent references (static: hardcoded at development time) ---

math_remote = RemoteA2aAgent(
    name="remote_math",
    description="Remote agent for arithmetic tasks",
    agent_card=f"http://127.0.0.1:8001{AGENT_CARD_WELL_KNOWN_PATH}",
)

prime_remote = RemoteA2aAgent(
    name="remote_prime",
    description="Remote agent that checks if numbers are prime",
    agent_card=f"http://127.0.0.1:8003{AGENT_CARD_WELL_KNOWN_PATH}",
)

# --- Coordinator: delegates to sub_agents based on user question ---

root_agent = Agent(
    name="coordinator",
    model=get_llm_model(),
    instruction=(
        "You are a coordinator agent. "
        "For arithmetic questions, delegate to remote_math. "
        "For prime-checking questions (e.g. 'is 17 prime?'), delegate to remote_prime."
    ),
    sub_agents=[math_remote, prime_remote],
)
