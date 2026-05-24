from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict, expire_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    exp = datetime.now(timezone.utc) + (expire_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode["exp"] = exp
    return jwt.encode(to_encode, settings.SECRETE_KEY, algorithm=settings.ALGORITHM)
    

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.SECRETE_KEY, algorithms=[settings.ALGORITHM])


