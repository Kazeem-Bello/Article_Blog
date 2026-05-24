from db.session import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Boolean, Column, Integer, String
from pydantic import EmailStr
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from models.blog_model import Blog
    



class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key = True)
    email: Mapped[EmailStr] = mapped_column(String(100), unique = True, index = True)
    hashed_password:Mapped[str] = mapped_column(nullable = False)
    is_active: Mapped[bool] = mapped_column(default = True)
    
    # many-to-one relationship (blog - user)
    blogs: Mapped[list["Blog"]] = relationship(back_populates = "author", cascade="all, delete-orphan")