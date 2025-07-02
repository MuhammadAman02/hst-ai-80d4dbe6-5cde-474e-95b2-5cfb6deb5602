"""User service for profile management."""

from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional, List
from app.models.user import User
from app.schemas.user import UserUpdate
from app.core.logging import get_logger

logger = get_logger("user_service")

class UserService:
    """Service for user operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        try:
            return self.db.get(User, user_id)
        except Exception as e:
            logger.error(f"Error getting user {user_id}: {e}")
            return None
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        try:
            stmt = select(User).where(User.email == email)
            return self.db.execute(stmt).scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error getting user by email {email}: {e}")
            return None
    
    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Update user profile."""
        try:
            user = self.get_user(user_id)
            if not user:
                return None
            
            update_data = user_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(user, field, value)
            
            self.db.commit()
            self.db.refresh(user)
            
            logger.info(f"User profile updated: {user_id}")
            return user
            
        except Exception as e:
            logger.error(f"Error updating user {user_id}: {e}")
            self.db.rollback()
            return None
    
    def search_users(self, query: str, limit: int = 20) -> List[User]:
        """Search users by name or email."""
        try:
            search_term = f"%{query}%"
            stmt = select(User).where(
                (User.first_name.ilike(search_term)) |
                (User.last_name.ilike(search_term)) |
                (User.email.ilike(search_term))
            ).limit(limit)
            
            result = self.db.execute(stmt)
            return result.scalars().all()
            
        except Exception as e:
            logger.error(f"Error searching users: {e}")
            return []
    
    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination."""
        try:
            stmt = select(User).offset(skip).limit(limit)
            result = self.db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error getting all users: {e}")
            return []

__all__ = ["UserService"]