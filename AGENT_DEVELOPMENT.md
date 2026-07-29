# Creating Custom Agents for The Orchestrator

This document explains how to build custom agents within the The Orchestrator system.

## Agent Structure Overview

Each agent extends BaseAgent and implements:
1. A specific workflow using LangGraph
2. Input/Output processing
3. State management

## Steps to Create a New Agent

### Step 1: Create an Agent Class

Create a new file in `app/agents/` with a class that inherits from BaseAgent:

```python
from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from app.agents.base_agent import BaseAgent, AgentState

class MyCustomAgentState(AgentState):
    """Define custom state for your agent"""
    # Add any specific fields needed
    task: str

def my_node(state: MyCustomAgentState) -> MyCustomAgentState:
    """Implement your processing logic"""
    print(f"Processing task: {state.task}")
    # Your implementation here
    return MyCustomAgentState(
        messages=state.messages + [{"role": "assistant", "content": f"Completed task: {state.task}"}],
        task=state.task,
        # Add any additional fields 
    )

class MyCustomAgent(BaseAgent):
    """A custom agent with its own workflow"""
    
    def __init__(self):
        super().__init__(
            name="My Custom Agent", 
            description="An agent that performs custom tasks"
        )
        
    def create_graph(self):
        """Define the agent's workflow"""
        workflow = StateGraph(MyCustomAgentState)
        workflow.add_node("process", my_node)
        workflow.set_entry_point("process")
        workflow.add_edge("process", END)
        return workflow.compile()
```

### Step 2: Register Your Agent

Add your agent to the manager:

```python
# In app/agents/manager.py
from app.agents.my_custom_agent import MyCustomAgent

class AgentManager:
    def _register_default_agents(self):
        """Register default agents"""
        self.agents["research"] = ResearchAgent
        self.agents["my_custom"] = MyCustomAgent  # Add this line
```

### Step 3: Use Your Agent

```python
# Using your new agent
from app.agents.manager import AgentManager

manager = AgentManager()
result = manager.run_agent("my_custom", {
    "messages": [{"role": "user", "content": "Start task"}],
    "task": "Important work to do"
})
```

## Available Tools and Integrations

The Orchestrator system supports:
- LangGraph for workflow management
- FastAPI for web interface 
- Ollama integration (localhost:11434 by default)
- Qdrant vector storage for embeddings
- Configuration management via settings

## Next Steps for You

To continue developing your own agents, consider:
1. Study existing agent implementations in the `app/agents` folder
2. Review LangGraph documentation to understand advanced workflows  
3. Define specific use cases for your custom agents
4. Test your agents with different types of inputs and scenarios

## Getting Started

I've already provided:
1. A base agent structure (`base_agent.py`)
2. A sample research agent (`research_agent.py`) 
3. An agent manager (`manager.py`)

You can now build upon these foundations to create your own specialized agents.