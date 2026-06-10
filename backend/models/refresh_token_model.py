from db.session import Base
from sqlalchemy import String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime, timezone
from typing import List, TYPE_CHECKING


if TYPE_CHECKING:
    from models.user_model import User
    from models.blog_model import Blog




class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    token: Mapped[str] = mapped_column(String(255), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    
    # many - one relationship (refresh_token - user)
    user: Mapped["User"] = relationship("User", back_populates="refresh_tokens")