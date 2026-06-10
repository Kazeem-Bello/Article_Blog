from passlib.context import CryptContext
from fastapi import HTTPException, status
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from core.config import settings
import re
from sqlalchemy.orm import Session
from models.user_model import User
from models.refresh_token_model import RefreshToken
from uuid import uuid4


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict, expire_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    exp = datetime.now(timezone.utc) + (expire_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode["exp"] = exp
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(detail="Token has expired", status_code=status.HTTP_401_UNAUTHORIZED)
    except JWTError:
        raise HTTPException(detail="Invalid token", status_code=status.HTTP_401_UNAUTHORIZED)


def validate_password(password: str):
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{5,}$"
    
    if not re.match(pattern, password):
        return False
    return password


    
    
