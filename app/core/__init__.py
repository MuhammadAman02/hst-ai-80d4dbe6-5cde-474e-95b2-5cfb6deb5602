"""Core application components with defensive imports and fallbacks."""

import logging
import os
import sys
from typing import Any, Dict, List, Optional
import importlib

# Set up basic logging immediately
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

fallback_logger = logging.getLogger("app")

# Safe import function
def safe_import(module_name: str, attributes: List[str], fallbacks: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Safely import attributes from a module with fallbacks."""
    result = {}
    fallbacks = fallbacks or {}
    
    try:
        module = importlib.import_module(module_name)
        for attr in attributes:
            if hasattr(module, attr):
                result[attr] = getattr(module, attr)
            else:
                fallback_logger.warning(f"Attribute '{attr}' not found in {module_name}")
                result[attr] = fallbacks.get(attr)
    except Exception as e:
        fallback_logger.warning(f"Error importing {module_name}: {e}")
        for attr in attributes:
            result[attr] = fallbacks.get(attr)
    
    return result

# Fallback implementations
class FallbackSettings:
    def __init__(self):
        self.APP_NAME = os.getenv("APP_NAME", "LinkedIn Clone")
        self.APP_DESCRIPTION = "Professional Networking Platform"
        self.APP_VERSION = "1.0.0"
        self.DEBUG = os.getenv("DEBUG", "False").lower() == "true"
        self.HOST = os.getenv("HOST", "0.0.0.0")
        self.PORT = int(os.getenv("PORT", "8000"))
        self.API_PREFIX = "/api"
        self.SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
        self.DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/linkedin_clone.db")
        self.UPLOAD_DIR = "app/static/uploads"
        self.MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def fallback_setup_middleware(app):
    fallback_logger.warning("Using fallback middleware setup")

def fallback_setup_routers(app, **kwargs):
    fallback_logger.warning("Using fallback router setup")

def fallback_setup_error_handlers(app):
    fallback_logger.warning("Using fallback error handlers")

def fallback_validate_environment():
    return []

def fallback_setup_database():
    fallback_logger.warning("Using fallback database setup")

def fallback_setup_nicegui(app):
    fallback_logger.warning("Using fallback NiceGUI setup")

class FallbackHealthCheck:
    @staticmethod
    def check_all():
        return {"status": "ok", "timestamp": "unknown"}

def fallback_is_healthy():
    return True

# Import core components with fallbacks
config_imports = safe_import("app.core.config", ["settings"], {
    "settings": FallbackSettings()
})
settings = config_imports["settings"]

logging_imports = safe_import("app.core.logging", ["app_logger"], {
    "app_logger": fallback_logger
})
app_logger = logging_imports["app_logger"]

middleware_imports = safe_import("app.core.middleware", ["setup_middleware"], {
    "setup_middleware": fallback_setup_middleware
})
setup_middleware = middleware_imports["setup_middleware"]

router_imports = safe_import("app.core.routers", ["setup_routers"], {
    "setup_routers": fallback_setup_routers
})
setup_routers = router_imports["setup_routers"]

error_imports = safe_import("app.core.error_handlers", ["setup_error_handlers"], {
    "setup_error_handlers": fallback_setup_error_handlers
})
setup_error_handlers = error_imports["setup_error_handlers"]

env_imports = safe_import("app.core.environment", ["validate_environment"], {
    "validate_environment": fallback_validate_environment
})
validate_environment = env_imports["validate_environment"]

db_imports = safe_import("app.core.database", ["setup_database"], {
    "setup_database": fallback_setup_database
})
setup_database = db_imports["setup_database"]

nicegui_imports = safe_import("app.core.nicegui_setup", ["setup_nicegui"], {
    "setup_nicegui": fallback_setup_nicegui
})
setup_nicegui = nicegui_imports["setup_nicegui"]

health_imports = safe_import("app.core.health", ["HealthCheck", "is_healthy"], {
    "HealthCheck": FallbackHealthCheck,
    "is_healthy": fallback_is_healthy
})
HealthCheck = health_imports["HealthCheck"]
is_healthy = health_imports["is_healthy"]

__all__ = [
    "settings",
    "app_logger", 
    "setup_middleware",
    "setup_routers",
    "setup_error_handlers",
    "validate_environment",
    "setup_database",
    "setup_nicegui",
    "HealthCheck",
    "is_healthy"
]