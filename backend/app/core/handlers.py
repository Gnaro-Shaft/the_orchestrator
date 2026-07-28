from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import OrchestratorException


async def orchestrator_exception_handler(
    request: Request,
    exc: OrchestratorException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.message,
            }
        },
    )