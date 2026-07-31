"""
Agents endpoint for The Orchestrator.
Handles agent status, execution, and management.
"""

from datetime import datetime
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.agents.manager import AgentManager

router = APIRouter()


class AgentRunRequest(BaseModel):
    agent_type: str
    inputs: dict[str, Any]


class AgentRunResponse(BaseModel):
    result: dict[str, Any]
    agent_type: str
    timestamp: str
    status: str


class AgentStatus(BaseModel):
    name: str
    status: str  # active, idle, error
    last_active: str | None = None
    current_task: str | None = None


@router.get("/agents/status")
async def get_agent_status():
    """Retourne le statut de tous les agents enregistrés."""
    try:
        manager = AgentManager()
        agents = manager.list_agents()

        agent_statuses = []
        for agent_name in agents:
            agent_statuses.append(AgentStatus(
                name=agent_name,
                status="active" if agent_name in ["research", "supervisor"] else "idle",
                last_active=datetime.now().astimezone().isoformat(),
                current_task=None,
            ))

        return {"agents": agent_statuses}

    except Exception:  # noqa: BLE001
        raise HTTPException(status_code=500, detail="Erreur")


@router.post("/agents/run", response_model=AgentRunResponse)
async def run_agent(request: AgentRunRequest):
    """Exécute un agent spécifique avec les entrées fournies."""
    try:
        manager = AgentManager()

        if request.agent_type not in manager.list_agents():
            raise HTTPException(
                status_code=404,
                detail=f"Agent '{request.agent_type}' non trouvé. Agents disponibles: {manager.list_agents()}",
            )

        agent = manager.get_agent(request.agent_type)
        result = agent.run(request.inputs)

        return AgentRunResponse(
            result=result,
            agent_type=request.agent_type,
            timestamp=datetime.now().astimezone().isoformat(),
            status="completed",
        )

    except HTTPException:
        raise
    except Exception:  # noqa: BLE001
        raise HTTPException(status_code=500, detail="Erreur d'exécution")


@router.get("/agents/list")
async def list_agents():
    """Liste tous les agents disponibles."""
    try:
        manager = AgentManager()
        return {"agents": manager.list_agents()}
    except Exception:  # noqa: BLE001
        raise HTTPException(status_code=500, detail="Erreur")
