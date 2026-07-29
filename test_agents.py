#!/usr/bin/env python3
"""
Test script for the orchestrator agents.
This demonstrates how to use and extend the agent system.
"""

import sys
import os

# Add the backend to the path 
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.agents.manager import AgentManager


def main():
    print("=== The Orchestrator Agent System ===")
    
    # Create an agent manager
    manager = AgentManager()
    
    # List available agents
    print("Available agents:", manager.list_agents())
    
    # Test the research agent
    print("\n--- Testing Research Agent ---")
    test_inputs = {
        "messages": [{"role": "user", "content": "Test query"}],
        "query": "Machine Learning Trends 2026"
    }
    
    try:
        result = manager.run_agent("research", test_inputs)
        print("Research agent completed successfully!")
        print("Result:", result)
    except Exception as e:
        print(f"Error running research agent: {e}")
        import traceback
        traceback.print_exc()
        
    print("\n=== System Ready ===")
    print("You can now create new agent types by:")
    print("1. Creating a new class that inherits from BaseAgent")
    print("2. Implementing the create_graph() method with your workflow")
    print("3. Registering it in the AgentManager")


if __name__ == "__main__":
    main()