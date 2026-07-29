"""
Base agent class for The Orchestrator.
This defines the common structure and methods for all agents in the system.
"""

from typing import Dict, Any, List
from pydantic import BaseModel


class AgentState(BaseModel):
    """Common state structure for agents"""
    messages: List[Dict[str, Any]]
    # Add any other common fields here


class BaseAgent:
    """Base class for all agents in the orchestrator system"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        
    def get_agent(self):
        """Get the configured agent for execution."""
        raise NotImplementedError("Subclasses must implement get_agent")
    
    def run(self, inputs: Dict[str, Any]):
        """Run the agent with given inputs."""
        agent = self.get_agent()
        return agent.invoke(inputs)