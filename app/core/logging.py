"""Logging configuration for the application."""

import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from typing import Dict, Any

# Configure the root logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Create application logger
app_logger = logging.getLogger("linkedin_clone")
app_logger.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
app_logger.addHandler(console_handler)

# File handler (if LOG_FILE is set)
log_file = os.getenv("LOG_FILE")
if log_file:
    try:
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5,
        )
        file_handler.setFormatter(formatter)
        app_logger.addHandler(file_handler)
    except Exception as e:
        app_logger.error(f"Failed to set up file logging: {e}")

def get_logger(name: str) -> logging.Logger:
    """Create a logger for a specific module."""
    return logging.getLogger(f"linkedin_clone.{name}")

def log_structured(logger: logging.Logger, level: str, message: str, data: Dict[str, Any]) -> None:
    """Log a message with structured data."""
    try:
        log_method = getattr(logger, level.lower(), logger.info)
        log_method(f"{message} - {data}")
    except Exception as e:
        logger.error(f"Error in log_structured: {e}")

__all__ = ["app_logger", "get_logger", "log_structured"]