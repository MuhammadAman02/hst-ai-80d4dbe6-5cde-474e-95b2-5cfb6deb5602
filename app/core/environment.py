"""Environment validation utilities."""

import os
from pathlib import Path
from typing import List
from app.core.logging import get_logger

logger = get_logger("environment")

def validate_environment() -> List[str]:
    """Validate environment configuration."""
    errors = []
    
    # Check required directories
    required_dirs = [
        "data",
        "app/static",
        "app/static/uploads"
    ]
    
    for dir_path in required_dirs:
        path = Path(dir_path)
        if not path.exists():
            try:
                path.mkdir(parents=True, exist_ok=True)
                logger.info(f"Created directory: {path}")
            except Exception as e:
                errors.append(f"Failed to create directory {path}: {e}")
    
    # Check environment variables
    if not os.getenv("SECRET_KEY") or os.getenv("SECRET_KEY") == "your-secret-key-change-in-production":
        logger.warning("Using default SECRET_KEY - change this in production!")
    
    return errors

__all__ = ["validate_environment"]