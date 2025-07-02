"""Database configuration and setup using SQLAlchemy V2."""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session
from app.core.config import settings
from app.core.logging import get_logger
import os

logger = get_logger("database")

# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_recycle=300
)

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass

def create_tables():
    """Create all database tables."""
    try:
        # Ensure data directory exists
        if "sqlite" in settings.DATABASE_URL:
            db_path = settings.DATABASE_URL.replace("sqlite:///", "")
            db_dir = os.path.dirname(db_path)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir, exist_ok=True)
        
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

def get_db() -> Session:
    """Database session dependency."""
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()

def setup_database():
    """Initialize database and create tables."""
    create_tables()

__all__ = ["Base", "engine", "get_db", "create_tables", "setup_database"]