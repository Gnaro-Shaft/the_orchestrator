"""
Agent manager for The Orchestrator.
Handles creation, registration, and execution of agents.
"""

from typing import Any

from app.agents.base_agent import BaseAgent
from app.agents.code_agent import CodeAgent
from app.agents.research_agent import ResearchAgent
from app.agents.supervisor import SupervisorAgent


class AgentManager:
    """Manages different types of agents in the orchestrator system."""

    def __init__(self):
        self.agents: dict[str, type[BaseAgent]] = {}
        self._register_default_agents()

    def _register_default_agents(self):
        """Register default agents."""
        self.agents["research"] = ResearchAgent
        self.agents["code"] = CodeAgent
        self.agents["supervisor"] = SupervisorAgent

    def register_agent(self, name: str, agent_class: type[BaseAgent]):
        """Register a new agent type."""
        self.agents[name] = agent_class

    def get_agent(self, agent_type: str) -> BaseAgent:
        """Get an instance of a specific agent type."""
        if agent_type not in self.agents:
            raise ValueError(f"Unknown agent type: {agent_type}. Available: {list(self.agents.keys())}")

        return self.agents[agent_type]()

    def list_agents(self) -> list[str]:
        """List all registered agents."""
        return list(self.agents.keys())

    def run_agent(self, agent_type: str, inputs: dict[str, Any]) -> dict[str, Any]:
        """Run a specific agent with given inputs."""
        agent = self.get_agent(agent_type)
        return agent.run(inputs)
