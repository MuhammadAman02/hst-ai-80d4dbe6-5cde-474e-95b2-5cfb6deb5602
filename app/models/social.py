"""Social networking models for connections, posts, and interactions."""

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Integer, DateTime, ForeignKey, Enum, func
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from enum import Enum as PyEnum
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.user import User

class ConnectionStatus(PyEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"

class Connection(Base):
    __tablename__ = "connections"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    requester_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    addressee_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    
    status: Mapped[ConnectionStatus] = mapped_column(Enum(ConnectionStatus), default=ConnectionStatus.PENDING)
    message: Mapped[str] = mapped_column(Text, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    requester: Mapped["User"] = relationship(foreign_keys=[requester_id], back_populates="sent_connections")
    addressee: Mapped["User"] = relationship(foreign_keys=[addressee_id], back_populates="received_connections")
    
    def __repr__(self) -> str:
        return f"<Connection(id={self.id}, requester_id={self.requester_id}, addressee_id={self.addressee_id}, status={self.status})>"

class Post(Base):
    __tablename__ = "posts"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    
    content: Mapped[str] = mapped_column(Text)
    image_url: Mapped[str] = mapped_column(String(255), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    author: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship(back_populates="post", cascade="all, delete-orphan")
    likes: Mapped[list["Like"]] = relationship(back_populates="post", cascade="all, delete-orphan")
    
    @property
    def like_count(self) -> int:
        """Get the number of likes for this post."""
        return len(self.likes)
    
    @property
    def comment_count(self) -> int:
        """Get the number of comments for this post."""
        return len(self.comments)
    
    def __repr__(self) -> str:
        return f"<Post(id={self.id}, user_id={self.user_id}, content='{self.content[:50]}...')>"

class Comment(Base):
    __tablename__ = "comments"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("posts.id"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    
    content: Mapped[str] = mapped_column(Text)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    post: Mapped["Post"] = relationship(back_populates="comments")
    author: Mapped["User"] = relationship(back_populates="comments")
    
    def __repr__(self) -> str:
        return f"<Comment(id={self.id}, post_id={self.post_id}, user_id={self.user_id})>"

class Like(Base):
    __tablename__ = "likes"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("posts.id"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    
    # Relationships
    post: Mapped["Post"] = relationship(back_populates="likes")
    user: Mapped["User"] = relationship(back_populates="likes")
    
    def __repr__(self) -> str:
        return f"<Like(id={self.id}, post_id={self.post_id}, user_id={self.user_id})>"

__all__ = ["Connection", "ConnectionStatus", "Post", "Comment", "Like"]