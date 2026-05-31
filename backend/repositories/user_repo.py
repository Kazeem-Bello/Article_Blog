from sqlalchemy.orm import Session
from sqlalchemy import select
from schemas.user_schema import UserCreate, UserPublic, UserUpdate
from models.user_model import User
from models.blog_model import Blog
from typing import List
from fastapi import HTTPException, status
from core.security import hash_password



class UserRepository:
    """all user database operations"""
    
    @staticmethod
    def create_user(user_in: UserCreate, db: Session) -> User:
        user = User(
            email=user_in.email,
            hashed_password=hash_password(user_in.password),
            username=user_in.username       
        )
        db.add(user)
        db.flush()
        db.refresh(user)
        return user
    
    @staticmethod
    def retrieve_users(db: Session):
        users = db.scalars(select(User)).all()
        return users
        
    
    @staticmethod
    def get_by_id(id: int, db: Session):
        user = db.scalars(select(User).where(User.id == id)).first()
        return user
    
    
    @staticmethod
    def get_by_email(email: str, db: Session):
        user = db.scalars(select(User).where(User.email == email)).first()
        return user
    
    
    @staticmethod
    def get_by_username(username: str, db: Session):
        user = db.scalars(select(User).where(User.username == username)).first()
        return user
    
    
    @staticmethod
    def update_user(id: int, user_in: UserUpdate, db: Session):
        user = db.scalars(select(User).where(User.id == id)).first()
        user_data = user_in.model_dump(exclude_unset=True)
        if "password" in user_data:
            user_data["hashed_password"] = hash_password(user_data["password"])
        user_data.pop("password")
        for key, value in user_data.items():
            setattr(user, key, value)        
        db.add(user)
        db.flush()
        db.refresh(user)
        return user
    
    
    @staticmethod
    def delete_user(id: int, db: Session):
        user = db.get(User, id)
        if not user:
            raise HTTPException(detail="User not found", status_code=status.HTTP_404_NOT_FOUND)
        db.delete(user)
        db.commit()
        return {"Message": "User Deleted"}
        