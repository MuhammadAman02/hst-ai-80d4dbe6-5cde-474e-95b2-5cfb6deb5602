"""Router configuration for the FastAPI application."""

from fastapi import FastAPI
from app.api.router import api_router
from app.core.logging import get_logger

logger = get_logger("routers")

def setup_routers(app: FastAPI, api_prefix: str = "/api") -> None:
    """Set up routers for the FastAPI application."""
    
    # Include API router
    app.include_router(api_router, prefix=api_prefix)
    
    logger.info(f"Routers configured with prefix: {api_prefix}")

__all__ = ["setup_routers"]