"""
Coordinator agent loader for ADK web.

ADK discovers agents by scanning subdirectories. Each subdir must have:
  - __init__.py (makes it a package)
  - agent.py with a root_agent (or app) variable

This file imports root_agent from coordinator_agent so ADK can load it.
The actual coordinator logic lives in coordinator_agent.py.
"""

from coordinator_agent import root_agent
