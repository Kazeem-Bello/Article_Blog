from db.session import SessionLocal, AsyncSessionLocal
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError
from core.security import decode_token
from pydantic import EmailStr
from repositories.user_repo import UserRepository
from models.user_model import User


def get_db():
    db = SessionLocal()
    try:
        yield db
        
    finally:
        db.close()
        
        
async def async_get_db():
    async with AsyncSessionLocal() as db:
        yield db
        
        
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/vi/auth/token")


def get_current_user(token: str, db: Session = Depends(get_db)):
    credential_exec = HTTPException(
        detail="Could not validate credentials", 
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={"WWW-Authorized": "Bearer"})
    try:
        payload = decode_token(token)
        email = payload.get("sub")  
        if not email:
            raise credential_exec
    except JWTError:
        raise credential_exec
    user = UserRepository.get_by_email(email=email, db=db)
    if not user:
        raise credential_exec
    return user
        
        
def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(detail="user is not active", status_code=status.HTTP_400_BAD_REQUEST)
    return current_user


def required_role(*role: str):
    def role_checker(current_user: User = Depends(get_current_active_user)):
        if current_user.role not in role:
            raise HTTPException(detail=f"Role required: {role}, user is {current_user.role}", status_code=status.HTTP_403_FORBIDDEN)
        return current_user
    return role_checker


require_admin = required_role("admin")
require_staff = required_role("admin", "moderator")