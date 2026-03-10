"""
Remote Prime Agent — A2A Server with a Tool

This agent checks if numbers are prime. It uses a function tool (check_prime)
that the LLM can call when the user asks about primality.

HOW IT WORKS:
  1. check_prime() is a tool: the LLM decides when to call it
  2. ADK auto-converts functions with type hints + docstrings into tools
  3. The agent uses the tool result to formulate its answer
  4. to_a2a() exposes this agent over the A2A protocol

RUN:
    uvicorn remote_prime_agent:a2a_app --host 127.0.0.1 --port 8003

NOTE:
    Uses port 8003 (different from math agent on 8001) so both can run.
"""

from dotenv import load_dotenv

load_dotenv()

from llm_config import get_llm_model
from google.adk.agents.llm_agent import Agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a


def check_prime(nums: list[int]) -> dict[int, bool]:
    """
    Check which numbers in the list are prime.

    This function becomes an ADK tool automatically. The LLM sees its
    signature and docstring, and can call it when the user asks about primes.

    Algorithm: for each n, test divisibility by integers from 2 to sqrt(n).
    Numbers < 2 are not prime.

    Args:
        nums: List of integers to check for primality.

    Returns:
        Dict mapping each input number to True (prime) or False (not prime).
        Example: check_prime([7, 8]) -> {7: True, 8: False}
    """
    result = {}
    for n in nums:
        if n < 2:
            result[n] = False
        else:
            # Only need to check up to sqrt(n)
            result[n] = all(n % i != 0 for i in range(2, int(n**0.5) + 1))
    return result


root_agent = Agent(
    name="prime_agent",
    model=get_llm_model(),
    instruction=(
        "You are a prime number expert. "
        "Use the check_prime tool to determine if numbers are prime. "
        "Answer clearly and briefly."
    ),
    tools=[check_prime],  # Register the function as a callable tool
)

a2a_app = to_a2a(root_agent, port=8003)



# This function does several things internally:
    # Wraps the agent into an A2A HTTP server
    # Generates the Agent Card metadata
    # Exposes the agent via FastAPI endpoints
    # Publishes the card at a well-known URL
# So the agent card is generated inside to_a2a().

# What to_a2a() Does Internally

# Conceptually it performs something like this:

# def to_a2a(agent):
#     agent_card = build_agent_card(agent)

#     app = FastAPI()

#     @app.get("/.well-known/agent.json")
#     def get_agent_card():
#         return agent_card

#     return app

# So the agent card endpoint becomes:
# http://127.0.0.1:8003/.well-known/agent.json



# What the Agent Card Contains

# The card describes the agent's capabilities and metadata.

# Example structure:

# {
#   "name": "prime_agent",
#   "description": "You are a prime number expert.",
#   "endpoint": "http://127.0.0.1:8003",
#   "skills": [
#     {
#       "name": "check_prime",
#       "description": "Check if numbers are prime",
#       "input_schema": {
#         "nums": "list[int]"
#       }
#     }
#   ]
# }

# ADK builds this automatically using:

# Agent.name

# Agent.instruction

# Agent.tools




# ADK inspects the function:

# def check_prime(nums: list[int]) -> dict[int, bool]:

# From this it extracts:

# Component	Extracted From
# Tool name	function name
# description	docstring
# parameters	type hints

# So the tool becomes an A2A skill.
# http://127.0.0.1:8003/.well-known/agent.json



# How ADK converts tools → skills

# ADK performs something conceptually like this:

# skill = AgentSkill(
#     name="check_prime",
#     description="Check which numbers are prime",
#     parameters={
#         "nums": "list[int]"
#     }
# )

# But this is generated internally.

# You do not need to write it yourself.

# 3. Your Agent Card automatically includes the skill

# If you open:

# http://127.0.0.1:8003/.well-known/agent.json

# you will see something like:

# {
#   "name": "prime_agent",
#   "skills": [
#     {
#       "name": "check_prime",
#       "description": "Check which numbers in the list are prime",
#       "parameters": {
#         "nums": "list[int]"
#       }
#     }
#   ]
# }

# So your function became an A2A skill.

# When you WOULD need AgentSkill

# You only define skills manually if you are using the low-level A2A SDK, not ADK.



    # skill = AgentSkill(
    #     id="insurance_coverage",
    #     name="Insurance coverage",
    #     description="Provides information about insurance coverage options and details.",
    #     tags=["insurance", "coverage"],
    #     examples=["What does my policy cover?", "Are mental health services included?"],
    # )

    # agent_card = AgentCard(
    #     name="InsurancePolicyCoverageAgent",
    #     description="Provides information about insurance policy coverage options and details.",
    #     url=f"http://{HOST}:{PORT}/",
    #     version="1.0.0",
    #     default_input_modes=["text"],
    #     default_output_modes=["text"],
    #     capabilities=AgentCapabilities(streaming=False),
    #     skills=[skill],
    # )