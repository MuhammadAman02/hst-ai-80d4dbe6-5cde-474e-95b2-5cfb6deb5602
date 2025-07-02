"""Social networking Pydantic schemas."""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional
from app.models.social import ConnectionStatus

class ConnectionCreate(BaseModel):
    """Schema for creating connection request."""
    addressee_id: int = Field(..., description="ID of user to connect with")
    message: Optional[str] = Field(None, max_length=500, description="Optional connection message")

class ConnectionResponse(BaseModel):
    """Schema for connection responses."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    requester_id: int
    addressee_id: int
    status: ConnectionStatus
    message: Optional[str] = None
    created_at: datetime

class PostCreate(BaseModel):
    """Schema for creating posts."""
    content: str = Field(..., min_length=1, max_length=3000, description="Post content")

class PostResponse(BaseModel):
    """Schema for post responses."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    content: str
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    like_count: int = 0
    comment_count: int = 0

class CommentCreate(BaseModel):
    """Schema for creating comments."""
    content: str = Field(..., min_length=1, max_length=1000, description="Comment content")

class CommentResponse(BaseModel):
    """Schema for comment responses."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    post_id: int
    user_id: int
    content: str
    created_at: datetime

__all__ = ["ConnectionCreate", "ConnectionResponse", "PostCreate", "PostResponse", "CommentCreate", "CommentResponse"]