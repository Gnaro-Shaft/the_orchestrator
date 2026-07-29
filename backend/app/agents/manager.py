"""
Agent manager for The Orchestrator.
This module handles the creation, registration, and execution of different agents.
"""

from typing import Dict, Type, Any, List
from app.agents.base_agent import BaseAgent
from app.agents.research_agent import ResearchAgent
from app.agents.code_agent import CodeAgent


class AgentManager:
    """Manages different types of agents in the orchestrator system"""
    
    def __init__(self):
        self.agents: Dict[str, Type[BaseAgent]] = {}
        self._register_default_agents()
    
    def _register_default_agents(self):
        """Register default agents"""
        self.agents["research"] = ResearchAgent
        self.agents["code"] = CodeAgent
    
    def register_agent(self, name: str, agent_class: Type[BaseAgent]):
        """Register a new agent type"""
        self.agents[name] = agent_class
        print(f"Registered agent: {name}")
    
    def get_agent(self, agent_type: str) -> BaseAgent:
        """Get an instance of a specific agent type"""
        if agent_type not in self.agents:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        return self.agents[agent_type]()
    
    def list_agents(self) -> List[str]:
        """List all registered agents"""
        return list(self.agents.keys())
    
    def run_agent(self, agent_type: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Run a specific agent with given inputs"""
        agent = self.get_agent(agent_type)
        return agent.run(inputs)