from sqlalchemy.orm import Session
from sqlalchemy import select
from models.refresh_token_model import RefreshToken
from models.user_model import User
from repositories.user_repo import UserRepository
from core.security import create_access_token
from datetime import datetime, timezone, timedelta
from core.config import settings
from uuid import uuid4


class RefreshTokenRepository:
    
    @staticmethod
    def create_tokens(db: Session, user: User):
        access_token = create_access_token(
            data = {"sub": str(user.id)}
        )
        refresh_token_str = str(uuid4())
        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        refresh_token = RefreshToken(
            user_id = user.id,
            token = refresh_token_str,
            expires_at = expires_at
        )
        db.add(refresh_token)
        db.commit()
        db.refresh(refresh_token)
        return {"access_token": access_token,
                "refresh_token": refresh_token_str,
                "token_type": "Bearer"}

    
    @staticmethod
    def verify_refresh_token(db: Session, token: str):
        refresh_token = db.scalars(select(RefreshToken).where(RefreshToken.token == token)).first()
        if refresh_token and not refresh_token.revoked:
            expires_at = refresh_token.expires_at
            if expires_at.tzinfo is None:
                expires_at = expires_at.replace(tzinfo=timezone.utc)
            if expires_at > datetime.now(timezone.utc):
                user = UserRepository.get_by_id(id=refresh_token.user_id, db=db)
                return user
            
    @staticmethod
    def create_email_token(user_id: int):
        to_encode = {"sub": str(user_id), "type": "verify_email"}
        email_token = create_access_token(data=to_encode, expire_delta=timedelta(hours=settings.EMAIL_VERIFICATION_TOKEN_EXPIRE_HOUR))
        return email_token
                
        
        
        
        