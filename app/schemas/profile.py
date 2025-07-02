"""Profile-related Pydantic schemas."""

from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from typing import Optional

class ExperienceBase(BaseModel):
    """Base experience schema."""
    company: str = Field(..., min_length=1, max_length=255)
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    location: Optional[str] = Field(None, max_length=255)
    start_date: date
    end_date: Optional[date] = None
    is_current: bool = False

class ExperienceCreate(ExperienceBase):
    """Schema for creating experience."""
    pass

class ExperienceResponse(ExperienceBase):
    """Schema for experience responses."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int

class EducationBase(BaseModel):
    """Base education schema."""
    school: str = Field(..., min_length=1, max_length=255)
    degree: Optional[str] = Field(None, max_length=255)
    field_of_study: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    start_date: date
    end_date: Optional[date] = None

class EducationCreate(EducationBase):
    """Schema for creating education."""
    pass

class EducationResponse(EducationBase):
    """Schema for education responses."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int

class SkillBase(BaseModel):
    """Base skill schema."""
    name: str = Field(..., min_length=1, max_length=100)

class SkillCreate(SkillBase):
    """Schema for creating skill."""
    pass

class SkillResponse(SkillBase):
    """Schema for skill responses."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    endorsements: int = 0

__all__ = ["ExperienceCreate", "ExperienceResponse", "EducationCreate", "EducationResponse", "SkillCreate", "SkillResponse"]