"""Error handlers for the FastAPI application."""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from app.core.logging import get_logger

logger = get_logger("error_handlers")

class AppError(Exception):
    """Base application error."""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class ValidationError(AppError):
    """Validation error."""
    def __init__(self, message: str):
        super().__init__(message, status_code=400)

class NotFoundError(AppError):
    """Resource not found error."""
    def __init__(self, message: str):
        super().__init__(message, status_code=404)

class UnauthorizedError(AppError):
    """Unauthorized access error."""
    def __init__(self, message: str):
        super().__init__(message, status_code=401)

def setup_error_handlers(app: FastAPI) -> None:
    """Set up error handlers for the FastAPI application."""
    
    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        logger.error(f"Application error: {exc.message}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.message}
        )
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        logger.warning(f"HTTP exception: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail}
        )
    
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"error": "An unexpected error occurred"}
        )
    
    logger.info("Error handlers configured successfully")

__all__ = ["setup_error_handlers", "AppError", "ValidationError", "NotFoundError", "UnauthorizedError"]