from fastapi import APIRouter

from app.api.routes.agents import router as agents_router
from app.api.routes.chat import router as chat_router
from app.api.routes.health import router as health_router
from app.api.routes.root import router as root_router

api_router = APIRouter()

api_router.include_router(root_router)
api_router.include_router(health_router, tags=["health"])
api_router.include_router(chat_router, tags=["chat"])
api_router.include_router(agents_router, tags=["agents"])