"""
Dynamic Coordinator Agent — discovers agents from registry at runtime

This is the SCALABLE (dynamic) orchestration pattern: remote agents are
loaded from a registry, not hardcoded. Add new agents by editing the
registry — no code change required.

HOW IT WORKS:
  1. load_agents_from_registry() reads agent definitions (file or HTTP)
  2. Each entry becomes a RemoteA2aAgent with name, description, agent_card URL
  3. The coordinator's sub_agents list is built at import time from the registry
  4. Same delegation behavior as static coordinator, but agents are pluggable

REGISTRY SOURCES (in order of precedence):
  - REGISTRY_URL env var → fetch JSON from HTTP (e.g. registry server)
  - agent_registry.json file → local file in project root

ADD A NEW AGENT:
  Edit agent_registry.json, add an entry:
    {"name": "...", "description": "...", "agent_card": "http://host:port/.well-known/agent-card.json"}

RUN:
    adk web . --port 8002
    Select "dynamic_coordinator" in the UI.
"""

import json
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from llm_config import get_llm_model
from google.adk.agents.llm_agent import Agent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

# Default: read from JSON file next to this module
REGISTRY_PATH = Path(__file__).parent / "agent_registry.json"


def load_agents_from_registry(
    registry_path: Path | str | None = None,
    registry_url: str | None = None,
) -> list[RemoteA2aAgent]:
    """
    Load RemoteA2aAgent instances from a registry (file or HTTP).

    Registry format:
        {"agents": [{"name": "...", "description": "...", "agent_card": "http://..."}]}

    Resolution order:
        1. registry_url arg (if provided)
        2. REGISTRY_URL env var (HTTP endpoint, e.g. http://localhost:8004/agents)
        3. registry_path arg or REGISTRY_PATH (local JSON file)

    Args:
        registry_path: Path to local JSON file. Default: agent_registry.json
        registry_url: HTTP URL that returns the registry JSON. Overrides file.

    Returns:
        List of RemoteA2aAgent instances, empty if registry not found or invalid.
    """
    agents_data = []

    # --- Try HTTP registry first (for real deployments) ---
    url = registry_url or os.getenv("REGISTRY_URL")
    if url:
        try:
            from urllib.request import urlopen
            with urlopen(url, timeout=10) as resp:
                data = json.loads(resp.read().decode())
            agents_data = data.get("agents", [])
        except Exception:
            # Network error, wrong URL, or invalid JSON — fall back to file
            pass

    # --- Fall back to local file ---
    if not agents_data:
        path = Path(registry_path or REGISTRY_PATH)
        if path.exists():
            data = json.loads(path.read_text())
            agents_data = data.get("agents", [])

    # Build RemoteA2aAgent for each registry entry
    return [
        RemoteA2aAgent(
            name=item["name"],
            description=item["description"],
            agent_card=item["agent_card"],
        )
        for item in agents_data
    ]


# --- Discover agents at runtime (not hardcoded) ---
sub_agents = load_agents_from_registry()

# Build instruction dynamically so the LLM knows what agents exist
agent_summary = ", ".join(f"{a.name} ({a.description})" for a in sub_agents) if sub_agents else "none"

root_agent = Agent(
    name="dynamic_coordinator",
    model=get_llm_model(),
    instruction=(
        "You are a coordinator agent. Delegate tasks to the appropriate sub-agent. "
        f"Available agents: {agent_summary}. "
        "Choose the best agent for each user request."
    ),
    sub_agents=sub_agents,
)
