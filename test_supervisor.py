"""
Test script for the Supervisor Agent.
This demonstrates how the main orchestrator works.
"""

import sys
import os

# Add the backend to the path 
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_supervisor():
    """Test the supervisor agent functionality"""
    
    print("=== Testing Supervisor Agent ===")
    
    try:
        from app.agents.manager import AgentManager
        
        # Create an agent manager
        manager = AgentManager()
        
        # List available agents
        print("Available agents:", manager.list_agents())
        
        # Test the supervisor agent specifically
        print("\n--- Testing Supervisor Agent ---")
        
        # Create test inputs
        test_inputs = {
            "messages": [{"role": "user", "content": "Test supervisor task"}],
            "current_task": "Research AI trends for 2026",
            "task_description": "Analyze current trends in artificial intelligence for the year 2026"
        }
        
        # Run the supervisor
        result = manager.run_agent("supervisor", test_inputs)
        
        print("Supervisor completed successfully!")
        print("Result:", result)
        
        print("\n=== Supervisor System Test Complete ===")
        print("The supervisor is ready to orchestrate multiple agents!")
        
    except Exception as e:
        print(f"Error during supervisor test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_supervisor()