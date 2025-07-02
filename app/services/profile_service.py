"""Profile service for managing professional information."""

from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional, List
from app.models.profile import Experience, Education, Skill
from app.schemas.profile import ExperienceCreate, EducationCreate, SkillCreate
from app.core.logging import get_logger

logger = get_logger("profile_service")

class ProfileService:
    """Service for profile operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    # Experience methods
    def add_experience(self, user_id: int, experience_create: ExperienceCreate) -> Optional[Experience]:
        """Add experience to user profile."""
        try:
            experience = Experience(
                user_id=user_id,
                **experience_create.model_dump()
            )
            
            self.db.add(experience)
            self.db.commit()
            self.db.refresh(experience)
            
            logger.info(f"Experience added for user {user_id}")
            return experience
            
        except Exception as e:
            logger.error(f"Error adding experience for user {user_id}: {e}")
            self.db.rollback()
            return None
    
    def get_user_experiences(self, user_id: int) -> List[Experience]:
        """Get all experiences for a user."""
        try:
            stmt = select(Experience).where(Experience.user_id == user_id).order_by(Experience.start_date.desc())
            result = self.db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error getting experiences for user {user_id}: {e}")
            return []
    
    # Education methods
    def add_education(self, user_id: int, education_create: EducationCreate) -> Optional[Education]:
        """Add education to user profile."""
        try:
            education = Education(
                user_id=user_id,
                **education_create.model_dump()
            )
            
            self.db.add(education)
            self.db.commit()
            self.db.refresh(education)
            
            logger.info(f"Education added for user {user_id}")
            return education
            
        except Exception as e:
            logger.error(f"Error adding education for user {user_id}: {e}")
            self.db.rollback()
            return None
    
    def get_user_education(self, user_id: int) -> List[Education]:
        """Get all education for a user."""
        try:
            stmt = select(Education).where(Education.user_id == user_id).order_by(Education.start_date.desc())
            result = self.db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error getting education for user {user_id}: {e}")
            return []
    
    # Skill methods
    def add_skill(self, user_id: int, skill_create: SkillCreate) -> Optional[Skill]:
        """Add skill to user profile."""
        try:
            # Check if skill already exists for user
            stmt = select(Skill).where(
                (Skill.user_id == user_id) & 
                (Skill.name.ilike(skill_create.name))
            )
            existing_skill = self.db.execute(stmt).scalar_one_or_none()
            
            if existing_skill:
                logger.warning(f"Skill '{skill_create.name}' already exists for user {user_id}")
                return existing_skill
            
            skill = Skill(
                user_id=user_id,
                name=skill_create.name
            )
            
            self.db.add(skill)
            self.db.commit()
            self.db.refresh(skill)
            
            logger.info(f"Skill added for user {user_id}: {skill_create.name}")
            return skill
            
        except Exception as e:
            logger.error(f"Error adding skill for user {user_id}: {e}")
            self.db.rollback()
            return None
    
    def get_user_skills(self, user_id: int) -> List[Skill]:
        """Get all skills for a user."""
        try:
            stmt = select(Skill).where(Skill.user_id == user_id).order_by(Skill.endorsements.desc())
            result = self.db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error getting skills for user {user_id}: {e}")
            return []

__all__ = ["ProfileService"]