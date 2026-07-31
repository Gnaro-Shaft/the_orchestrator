"""
Models module for The Orchestrator.

Pydantic data models shared across the application.
"""

from typing import Any

from pydantic import BaseModel


class Conversation(BaseModel):
    """Represents a conversation thread."""
    id: str | None = None
    title: str = ""
    messages: list[dict[str, Any]] = []
    created_at: str = ""
    updated_at: str = ""

    model_config = {"populate_by_name": True}


class AgentLog(BaseModel):
    """Log entry for agent execution."""
    agent_name: str
    task: str
    result: str
    status: str = "success"
    timestamp: str = ""


class SystemConfig(BaseModel):
    """Application-wide configuration."""
    default_model: str = "llama3"
    ollama_url: str = "http://localhost:11434"
    qdrant_url: str = "http://localhost:6333"
    debug: bool = False
