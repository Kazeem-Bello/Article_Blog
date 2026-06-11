from core.security import verify_password, validate_password, decode_token, hash_password
from models.user_model import User
from schemas.user_schema import UserCreate, PasswordChange, PasswordReset
from db.deps import get_db
from sqlalchemy.orm import Session
from repositories.user_repo import UserRepository
from fastapi import HTTPException, status, Request
from fastapi.responses import JSONResponse
from core.config import settings
from datetime import timedelta
from schemas.auth import Token
from repositories.refresh_token_repo import RefreshTokenRepository



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
                detail="Password must be at least 8 characters long, contains one uppercase letter, "
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
    def refresh_token(request: Request, db: Session):
        token = request.cookies.get("refresh_token")
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
        if not payload  or payload.get("type") != "verify_email":
            raise HTTPException(
                detail="Invalid or missing token",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        user_id = int(payload.get("sub"))
        user = UserRepository.get_by_id(db=db, id=user_id)
        if not user: 
            raise HTTPException(
                detail="User not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        user.is_verified = True
        db.add(user)
        db.commit()
        return {"message": "Verification successful!!"}
        
        
    @staticmethod
    def change_password(password: PasswordChange, user: User, db: Session):
        if not verify_password(password.old_password, user.hashed_password):
            raise HTTPException(detail="Old password is not correct", status_code=status.HTTP_401_UNAUTHORIZED)
        if not validate_password(password.new_password):
            raise HTTPException(
                detail=" New password must be at least 8 characters long, contains one uppercase letter, "
            "one lowercase letter, one number, and one special character",
                status_code=status.HTTP_400_BAD_REQUEST,
            ) 
        user = UserRepository.change_password(password=password, user=user, db=db)
        return {"Message": "Password changed successfully"}
    
    
    @staticmethod
    def send_password_reset_token(email: str, db: Session):
        user = UserRepository.get_by_email(email=email, db=db)
        if not user:
            raise HTTPException(
                detail="User not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        password_token = RefreshTokenRepository.create_password_reset_token(user_id=user.id)
        link = f"http://localhost:8000/reset?token={password_token}"
        print(f"Reset your password: {link}")
        return {"message": "Password Reset sent"}
    
    
    @staticmethod
    def reset_password(password: PasswordReset, db: Session):
        payload = decode_token(password.token)
        if not payload or payload.get("type") != "reset_password":
            raise HTTPException(
                detail="Invalid or missing token",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        user_id = int(payload.get("sub"))
        user = UserRepository.get_by_id(db=db, id=user_id)
        if not user: 
            raise HTTPException(
                detail="User not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        if not validate_password(password.new_password):
            raise HTTPException(
                detail=" New password must be at least 8 characters long, contains one uppercase letter, "
            "one lowercase letter, one number, and one special character",
                status_code=status.HTTP_400_BAD_REQUEST,
            ) 
        user.hashed_password = hash_password(password.new_password)
        db.add(user)
        db.commit()
        return {"message": "Password reset successfully!!"}
    
    @staticmethod
    def revoke_refresh_token(request: Request, db: Session):
        token = request.cookies.get("refresh_token")
        if not token:
            raise HTTPException(
                detail="Invalid or missing token",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        revoked_token = RefreshTokenRepository.revoke_refresh_token(token=token, db=db)
        response = JSONResponse(content = {"message": "Logged out successfully"})
        response.delete_cookie("refresh_token")
        response.delete_cookie("access_token")
        return response