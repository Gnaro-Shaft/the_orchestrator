"""
Chat endpoint for The Orchestrator.
Handles communication between users and agents via the supervisor.
"""

from datetime import datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.agents.supervisor import SupervisorAgent, SupervisorState

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    context: str | None = None
    agent_type: str | None = None


class ChatResponse(BaseModel):
    response: str
    agent_used: str
    timestamp: str
    status: str


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Endpoint principal pour communiquer avec les agents.
    Le superviseur analyse la requête et route vers l'agent approprié.
    """
    try:
        supervisor = SupervisorAgent()

        state = SupervisorState(
            messages=[{"role": "user", "content": request.message}],
            current_task=request.message,
            task_description=request.context or request.message,
            agent_responses=[],
            final_output="",
            task_status="processing",
        )

        agent = supervisor.get_agent()

        if agent is None:
            result = supervisor.run({
                "current_task": request.message,
                "task_description": request.context or request.message,
            })

            return ChatResponse(
                response=result.get("final_output", "Réponse du superviseur"),
                agent_used="supervisor",
                timestamp=datetime.now().astimezone().isoformat(),
                status=result.get("status", "completed"),
            )
        else:
            result = agent.invoke(state)

            return ChatResponse(
                response=result.final_output if hasattr(result, "final_output") else "Traitement en cours",
                agent_used="supervisor",
                timestamp=datetime.now().astimezone().isoformat(),
                status=result.task_status if hasattr(result, "task_status") else "completed",
            )

    except Exception:  # noqa: BLE001
        raise HTTPException(status_code=500, detail="Erreur du superviseur")


@router.get("/health")
async def health_check():
    """Point de contrôle de santé de l'API"""
    return {
        "status": "healthy",
        "service": "The Orchestrator API",
        "version": "0.1.0",
    }
