from core.security import verify_password
from models.user_model import User
from schemas.user_schema import UserCreate
from db.deps import get_db
from sqlalchemy.orm import Session
from repositories.user_repo import UserRepository
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from core.config import settings
from datetime import timedelta
from schemas.auth import Token
from core.security import validate_password
from repositories.refresh_token_repo import RefreshTokenRepository
from core.security import decode_token



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
        if not validate_password(user_in.password):
            raise HTTPException(
                detail="Password must be at least 8 characters long and contain one uppercase letter, "
            "one lowercase letter, one number, and one special character",
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
        tokens = RefreshTokenRepository.create_tokens(
            db=db,
            user=user            
        )
        response = JSONResponse(content= {"message": "Login Successful!!", "access_token": tokens["access_token"]})
        response.set_cookie(
            "access_token",
            value=tokens["access_token"],
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=60*60*24*1)
        response.set_cookie(
            "refresh_token",
            value=tokens["refresh_token"],
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=60*60*24*7)
        return response
    
    
    @staticmethod
    def refresh_token(token: str, db: Session):
        user = RefreshTokenRepository.verify_refresh_token(token=token, db=db)
        if not user:
            raise HTTPException(
                detail="Invalid or missing token",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        
        tokens = RefreshTokenRepository.create_tokens(
            db=db,
            user=user            
        )
        response = JSONResponse(content= {"message": "Token refreshed successfully"})
        response.set_cookie(
            "access_token",
            value=tokens["access_token"],
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=60*60*24*1)
        response.set_cookie(
            "refresh_token",
            value=tokens["refresh_token"],
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=60*60*24*7)
        return response
        
        
    @staticmethod
    def send_email_verification_token(user: User):
        email_token = RefreshTokenRepository.create_email_token(user_id=user.id)
        link = f"http://localhost:8000/verify?token={email_token}"
        print(f"verify your email: {link}")
        return {"message": "Email verification sent"}
            
    
    @staticmethod
    def verify_email(db: Session, token: str):
        payload = decode_token(token)
        if not payload and payload.get("type") != "verify_email":
            raise HTTPException(
                detail="Invalid or missing token",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        user_id = int(payload.get("sub"))
        user = UserRepository.get_by_id(db=db, id=user_id)
        if not user: 
            raise HTTPException(
                detail="User no found",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        user.is_verified = True
        db.add(user)
        db.commit()
        return {"message": "Verification successful!!"}
        
        
        