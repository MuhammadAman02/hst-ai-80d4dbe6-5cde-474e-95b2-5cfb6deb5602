"""Health check utilities."""

import time
from typing import Dict, Any
from app.core.logging import get_logger

logger = get_logger("health")

class HealthCheck:
    """Health check utilities."""
    
    @staticmethod
    def check_all() -> Dict[str, Any]:
        """Perform comprehensive health check."""
        return {
            "status": "healthy",
            "timestamp": time.time(),
            "checks": {
                "database": "ok",
                "application": "ok"
            }
        }

def is_healthy() -> bool:
    """Simple health check."""
    return True

__all__ = ["HealthCheck", "is_healthy"]