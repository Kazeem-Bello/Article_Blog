from db.session import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Text, func
from pydantic import EmailStr
from typing import List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from models.user_model import User
    



class Blog(Base):
    __tablename__ = "blogs"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable = True)
    created_at: Mapped[datetime] = mapped_column(default = datetime.now)
    is_active: Mapped[bool] = mapped_column(default=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    
    # many-to-one relationship (blog - user)
    author: Mapped["User"] = relationship(back_populates="blogs")
    