"""Authentication service for user login and registration."""

from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.logging import get_logger

logger = get_logger("auth_service")

class AuthService:
    """Service for authentication operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def register_user(self, user_create: UserCreate) -> Optional[User]:
        """Register a new user."""
        try:
            # Check if user already exists
            stmt = select(User).where(User.email == user_create.email)
            existing_user = self.db.execute(stmt).scalar_one_or_none()
            
            if existing_user:
                logger.warning(f"Registration attempt with existing email: {user_create.email}")
                return None
            
            # Create new user
            hashed_password = get_password_hash(user_create.password)
            db_user = User(
                email=user_create.email,
                first_name=user_create.first_name,
                last_name=user_create.last_name,
                hashed_password=hashed_password
            )
            
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            
            logger.info(f"New user registered: {user_create.email}")
            return db_user
            
        except Exception as e:
            logger.error(f"Error registering user: {e}")
            self.db.rollback()
            return None
    
    def authenticate_user(self, user_login: UserLogin) -> Optional[User]:
        """Authenticate user credentials."""
        try:
            stmt = select(User).where(User.email == user_login.email)
            user = self.db.execute(stmt).scalar_one_or_none()
            
            if not user or not verify_password(user_login.password, user.hashed_password):
                logger.warning(f"Failed authentication attempt for: {user_login.email}")
                return None
            
            if not user.is_active:
                logger.warning(f"Authentication attempt for inactive user: {user_login.email}")
                return None
            
            logger.info(f"User authenticated successfully: {user_login.email}")
            return user
            
        except Exception as e:
            logger.error(f"Error authenticating user: {e}")
            return None
    
    def create_user_token(self, user: User) -> str:
        """Create access token for user."""
        token_data = {"sub": str(user.id), "email": user.email}
        return create_access_token(token_data)

__all__ = ["AuthService"]