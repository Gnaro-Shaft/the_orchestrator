from fastapi import FastAPI

from app.api.router import api_router
from app.config.settings import get_settings
from app.core.logging import setup_logging
from app.core.exceptions import OrchestratorException
from app.core.handlers import orchestrator_exception_handler

import logging


setup_logging()
settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.add_exception_handler(
    OrchestratorException,
    orchestrator_exception_handler,
)

logger = logging.getLogger(__name__)

logger.info("The Orchestrator API started")

app.include_router(api_router, prefix=settings.api_prefix)