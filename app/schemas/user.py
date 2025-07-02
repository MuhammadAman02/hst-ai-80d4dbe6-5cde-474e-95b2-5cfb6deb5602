"""User-related Pydantic schemas."""

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    """Base user schema with common fields."""
    email: EmailStr = Field(..., description="User email address")
    first_name: str = Field(..., min_length=1, max_length=100, description="First name")
    last_name: str = Field(..., min_length=1, max_length=100, description="Last name")

class UserCreate(UserBase):
    """Schema for user registration."""
    password: str = Field(..., min_length=8, description="User password")

class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")

class UserUpdate(BaseModel):
    """Schema for user profile updates."""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    headline: Optional[str] = Field(None, max_length=255)
    summary: Optional[str] = Field(None, max_length=2000)
    location: Optional[str] = Field(None, max_length=255)

class UserResponse(UserBase):
    """Schema for user responses."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    headline: Optional[str] = None
    summary: Optional[str] = None
    profile_image: Optional[str] = None
    location: Optional[str] = None
    is_active: bool
    created_at: datetime

class UserProfile(UserResponse):
    """Extended user profile with additional information."""
    full_name: str
    
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    """Schema for authentication token response."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

__all__ = ["UserCreate", "UserLogin", "UserUpdate", "UserResponse", "UserProfile", "TokenResponse"]