"""
Simple research agent for The Orchestrator.
This agent demonstrates how to build a specialized agent using LangGraph.
"""

from typing import Dict, Any, List
from pydantic import BaseModel
from app.agents.base_agent import BaseAgent, AgentState


class ResearchAgentState(AgentState):
    """State structure specific to the research agent"""
    query: str
    research_results: List[str]
    summary: str


def research_node(state: ResearchAgentState) -> ResearchAgentState:
    """Research node - simulates research work"""
    # In a real implementation, this would call an LLM or external API
    print(f"Researching: {state.query}")
    
    results = [
        f"Result 1 for '{state.query}'",
        f"Result 2 for '{state.query}'",
        f"Result 3 for '{state.query}'"
    ]
    
    return ResearchAgentState(
        messages=state.messages + [{"role": "assistant", "content": f"Completed research on '{state.query}'"}],
        query=state.query,
        research_results=results,
        summary=""
    )


def summarize_node(state: ResearchAgentState) -> ResearchAgentState:
    """Summarize node - creates a summary from research results"""
    print("Summarizing research results...")
    
    summary = f"Summary of research on '{state.query}': " + \
              ", ".join(state.research_results[:2])
    
    return ResearchAgentState(
        messages=state.messages + [{"role": "assistant", "content": "Completed summarization"}],
        query=state.query,
        research_results=state.research_results,
        summary=summary
    )


class ResearchAgent(BaseAgent):
    """Research agent that performs fact gathering and summarization"""
    
    def __init__(self):
        super().__init__(
            name="Research Agent", 
            description="An agent that researches topics and summarizes findings"
        )
        
    def get_agent(self):
        """Get the configured agent for execution."""
        try:
            from langgraph.graph import StateGraph, END
            # Define the workflow
            workflow = StateGraph(ResearchAgentState)
            
            workflow.add_node("research", research_node)
            workflow.add_node("summarize", summarize_node)
            
            # Define the edges - using proper LangGraph syntax
            workflow.set_entry_point("research")
            workflow.add_edge("research", "summarize")
            workflow.add_edge("summarize", END)
            
            return workflow.compile()
        except ImportError:
            print("LangGraph not available - research agent will not function properly in this test")
            # Return a basic implementation for testing purposes
            return None