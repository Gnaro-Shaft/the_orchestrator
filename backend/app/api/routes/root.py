from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def root():
    return {
        "name": "The Orchestrator API",
        "version": "0.1.0",
    }