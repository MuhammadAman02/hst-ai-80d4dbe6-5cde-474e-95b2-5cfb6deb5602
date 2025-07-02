"""User model for authentication and basic profile information."""

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, DateTime, Text, func
from datetime import datetime
from typing import List, TYPE_CHECKING
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.profile import Experience, Education, Skill
    from app.models.social import Connection, Post, Comment, Like

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    
    # Profile information
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    headline: Mapped[str] = mapped_column(String(255), nullable=True)
    summary: Mapped[str] = mapped_column(Text, nullable=True)
    profile_image: Mapped[str] = mapped_column(String(255), nullable=True)
    location: Mapped[str] = mapped_column(String(255), nullable=True)
    
    # Account status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    experiences: Mapped[List["Experience"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    education: Mapped[List["Education"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    skills: Mapped[List["Skill"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    posts: Mapped[List["Post"]] = relationship(back_populates="author", cascade="all, delete-orphan")
    comments: Mapped[List["Comment"]] = relationship(back_populates="author", cascade="all, delete-orphan")
    likes: Mapped[List["Like"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    
    # Connection relationships
    sent_connections: Mapped[List["Connection"]] = relationship(
        foreign_keys="Connection.requester_id",
        back_populates="requester",
        cascade="all, delete-orphan"
    )
    received_connections: Mapped[List["Connection"]] = relationship(
        foreign_keys="Connection.addressee_id", 
        back_populates="addressee",
        cascade="all, delete-orphan"
    )
    
    @property
    def full_name(self) -> str:
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}', name='{self.full_name}')>"

__all__ = ["User"]