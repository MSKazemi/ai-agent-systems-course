"""
Dynamic coordinator agent loader for ADK web.

Same pattern as coordinator/: this package exists so ADK can discover
the agent. The real logic (registry loading, agent creation) is in
dynamic_coordinator_agent.py.
"""

from dynamic_coordinator_agent import root_agent
