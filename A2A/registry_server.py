"""
Agent Registry API — HTTP endpoint for agent discovery

In production A2A systems, agents are often discovered via an HTTP registry
instead of a local file. This module provides a minimal registry server.

HOW IT WORKS:
  - Serves the contents of agent_registry.json at GET /agents
  - The dynamic coordinator can set REGISTRY_URL to this endpoint
  - Enables central registry: one service lists all available agents

USE CASE:
  - Multiple coordinators can share the same registry
  - Registry can be updated without redeploying coordinators
  - Foundation for auth, versioning, or filtering later

RUN:
    uvicorn registry_server:app --host 127.0.0.1 --port 8004

CONFIGURE DYNAMIC COORDINATOR:
    Add to .env: REGISTRY_URL=http://127.0.0.1:8004/agents
"""

import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import JSONResponse

REGISTRY_PATH = Path(__file__).parent / "agent_registry.json"

app = FastAPI(title="A2A Agent Registry")


@app.get("/")
def root():
    """Health/info endpoint."""
    return {"message": "A2A Agent Registry", "agents": "/agents"}


@app.get("/agents")
def get_agents():
    """
    Return the list of available agents.

    Response format (same as agent_registry.json):
        {"description": "...", "agents": [{"name": "...", "description": "...", "agent_card": "..."}]}

    The dynamic coordinator parses this and creates RemoteA2aAgent instances.
    """
    if not REGISTRY_PATH.exists():
        return JSONResponse({"agents": []})
    data = REGISTRY_PATH.read_text()
    return JSONResponse(json.loads(data))
