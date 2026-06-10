from db.session import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from datetime import datetime, timezone
from typing import List, TYPE_CHECKING


if TYPE_CHECKING:
    from models.blog_model import Blog
    from models.refresh_token_model import RefreshToken
    



class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    hashed_password:Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    
    # one-to-many relationship (user - blog)
    blogs: Mapped[List["Blog"]] = relationship(back_populates="author", cascade="all, delete-orphan")
    # one-to-many relationship (user - refresh_token)
    refresh_tokens: Mapped[List["RefreshToken"]] = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")