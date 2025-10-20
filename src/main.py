import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator, Optional

from fastapi import FastAPI

from src.config.settings import settings
from src.services.health_service import HealthService
from src.services.item_service import ItemService

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan handler."""
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    yield
    logger.info(f"Shutting down {settings.app_name}")


app = FastAPI(title=settings.app_name, version=settings.app_version, lifespan=lifespan)


@app.get("/")
async def root() -> dict:
    """Root endpoint."""
    return {"message": f"Welcome to {settings.app_name}"}


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return HealthService.get_health_status()


@app.get("/ready")
async def readiness_check() -> dict:
    """Readiness check endpoint."""
    return HealthService.get_readiness_status()


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None) -> dict:
    """Get item by ID."""
    return ItemService.get_item(item_id, q)
