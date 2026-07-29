"""
Communication system for The Orchestrator agents.
This enables agents to exchange information and coordinate their actions.
"""

from typing import Dict, Any, List
from pydantic import BaseModel
import json


class AgentMessage(BaseModel):
    """Represents a message sent between agents"""
    sender: str
    recipient: str
    content: str
    message_type: str  # 'request', 'response', 'notification'
    metadata: Dict[str, Any] = {}
    timestamp: str = ""


class CommunicationManager:
    """Manages communication between agents in the orchestrator system"""
    
    def __init__(self):
        self.message_queue: List[AgentMessage] = []
        self.agent_memory: Dict[str, Dict[str, Any]] = {}
        
    def send_message(self, sender: str, recipient: str, content: str, 
                    message_type: str = "request", metadata: Dict[str, Any] = None) -> AgentMessage:
        """Send a message from one agent to another"""
        if metadata is None:
            metadata = {}
            
        message = AgentMessage(
            sender=sender,
            recipient=recipient,
            content=content,
            message_type=message_type,
            metadata=metadata
        )
        
        self.message_queue.append(message)
        print(f"✓ Message sent: {sender} -> {recipient}")
        return message
    
    def receive_message(self, recipient: str) -> List[AgentMessage]:
        """Receive messages intended for a specific agent"""
        received_messages = [
            msg for msg in self.message_queue 
            if msg.recipient == recipient
        ]
        
        # Remove messages that were received
        self.message_queue = [
            msg for msg in self.message_queue 
            if msg.recipient != recipient
        ]
        
        return received_messages
    
    def store_memory(self, agent_name: str, key: str, value: Any) -> None:
        """Store information in agent memory"""
        if agent_name not in self.agent_memory:
            self.agent_memory[agent_name] = {}
        
        self.agent_memory[agent_name][key] = value
        print(f"✓ Memory stored: {agent_name}.{key}")
    
    def retrieve_memory(self, agent_name: str, key: str) -> Any:
        """Retrieve information from agent memory"""
        if agent_name in self.agent_memory and key in self.agent_memory[agent_name]:
            return self.agent_memory[agent_name][key]
        return None
    
    def broadcast_message(self, sender: str, content: str, 
                         message_type: str = "notification") -> List[AgentMessage]:
        """Send a message to all agents"""
        # In a real implementation, this would get all registered agents
        # For now we simulate it with a list of common agents
        target_agents = ["research", "code", "supervisor"]
        messages = []
        
        for agent in target_agents:
            if agent != sender:  # Don't send to self
                msg = self.send_message(sender, agent, content, message_type)
                messages.append(msg)
                
        return messages
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get current system status"""
        return {
            "message_queue_size": len(self.message_queue),
            "agents_with_memory": list(self.agent_memory.keys()),
            "total_messages": len(self.message_queue)
        }


# Global communication instance
communication_manager = CommunicationManager()


def send_agent_message(sender: str, recipient: str, content: str, 
                      message_type: str = "request", metadata: Dict[str, Any] = None) -> AgentMessage:
    """Convenience function to send a message"""
    if metadata is None:
        metadata = {}
    return communication_manager.send_message(sender, recipient, content, message_type, metadata)


def receive_agent_messages(recipient: str) -> List[AgentMessage]:
    """Convenience function to receive messages for an agent"""
    return communication_manager.receive_message(recipient)


def store_agent_memory(agent_name: str, key: str, value: Any) -> None:
    """Convenience function to store agent memory"""
    communication_manager.store_memory(agent_name, key, value)


def retrieve_agent_memory(agent_name: str, key: str) -> Any:
    """Convenience function to retrieve agent memory"""
    return communication_manager.retrieve_memory(agent_name, key)


def broadcast_system_message(sender: str, content: str, 
                           message_type: str = "notification") -> List[AgentMessage]:
    """Broadcast a message to all agents"""
    return communication_manager.broadcast_message(sender, content, message_type)