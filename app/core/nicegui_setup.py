"""NiceGUI integration setup."""

from fastapi import FastAPI
from app.core.logging import get_logger

logger = get_logger("nicegui_setup")

def setup_nicegui(app: FastAPI) -> None:
    """Set up NiceGUI integration with FastAPI."""
    logger.info("NiceGUI integration configured")

__all__ = ["setup_nicegui"]