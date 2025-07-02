"""Profile-related models for professional information."""

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Integer, Date, Boolean, ForeignKey
from datetime import date
from typing import Optional, TYPE_CHECKING
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.user import User

class Experience(Base):
    __tablename__ = "experiences"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    
    company: Mapped[str] = mapped_column(String(255))
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    location: Mapped[str] = mapped_column(String(255), nullable=True)
    
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    is_current: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Relationships
    user: Mapped["User"] = relationship(back_populates="experiences")
    
    def __repr__(self) -> str:
        return f"<Experience(id={self.id}, title='{self.title}', company='{self.company}')>"

class Education(Base):
    __tablename__ = "education"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    
    school: Mapped[str] = mapped_column(String(255))
    degree: Mapped[str] = mapped_column(String(255), nullable=True)
    field_of_study: Mapped[str] = mapped_column(String(255), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    # Relationships
    user: Mapped["User"] = relationship(back_populates="education")
    
    def __repr__(self) -> str:
        return f"<Education(id={self.id}, school='{self.school}', degree='{self.degree}')>"

class Skill(Base):
    __tablename__ = "skills"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    
    name: Mapped[str] = mapped_column(String(100))
    endorsements: Mapped[int] = mapped_column(Integer, default=0)
    
    # Relationships
    user: Mapped["User"] = relationship(back_populates="skills")
    
    def __repr__(self) -> str:
        return f"<Skill(id={self.id}, name='{self.name}', endorsements={self.endorsements})>"

__all__ = ["Experience", "Education", "Skill"]