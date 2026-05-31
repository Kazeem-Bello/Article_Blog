from core.security import create_access_token, verify_password
from models.user_model import User
from schemas.user_schema import UserCreate
from db.deps import get_db
from sqlalchemy.orm import Session
from repositories.user_repo import UserRepository
from fastapi import HTTPException, status
from pydantic import EmailStr
from core.config import settings
from datetime import timedelta
from schemas.auth import Token



class AuthServices:
    
    @staticmethod
    def register(user_in: UserCreate, db: Session):
        if UserRepository.get_by_email(email=user_in.email, db=db):
            raise HTTPException(
                detail="Email already registered",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        if UserRepository.get_by_username(username=user_in.username, db=db):
            raise HTTPException(
                detail="Username not available",
                status_code=status.HTTP_400_BAD_REQUEST,
            )  
        user = UserRepository.create_user(user_in=user_in, db=db)
        db.commit()     
        return user
    
    
    @staticmethod
    def login(username_or_email: str, password: str, db: Session):
        user = UserRepository.get_by_email(email=username_or_email, db=db)
        if not user: 
            user = UserRepository.get_by_username(username=username_or_email, db=db)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                detail="Incorrect credentials", 
                status_code=status.HTTP_401_UNAUTHORIZED, 
                headers={"WWW-Authenticate": "Bearer"}
            )
        token = create_access_token(
            data={"sub": user.email}, #you can add other info like user.role in data
            expire_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) 
            )
        return Token(access_token=token, token_type="Bearer")
        
        