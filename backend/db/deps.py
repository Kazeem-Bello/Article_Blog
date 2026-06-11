from db.session import SessionLocal, AsyncSessionLocal
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
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
        
        
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")


def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token") 
    if not token:
        raise HTTPException(detail="Missing access token", status_code=status.HTTP_401_UNAUTHORIZED, headers={"WWW-Authenticate": "Bearer"})
    payload = decode_token(token)
    user_id = int(payload.get("sub"))
    if not user_id: 
        raise HTTPException(detail="Invalid token", status_code=status.HTTP_401_UNAUTHORIZED, headers={"WWW-Authenticate": "Bearer"})
    user = UserRepository.get_by_id(id=user_id, db=db)
    if not user:
        raise HTTPException(detail="User not found", status_code=status.HTTP_401_UNAUTHORIZED, headers={"WWW-Authenticate": "Bearer"})
    return user
        
    
        
        
def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(detail="user is not active", status_code=status.HTTP_400_BAD_REQUEST)
    return current_user


def require_admin(user: User = Depends(get_current_active_user)):
    if not user.is_admin:
        raise HTTPException(detail=f"Administrative access required", status_code=status.HTTP_403_FORBIDDEN)
    return user
        
        
def required_role(*role: str):
    def role_checker(current_user: User = Depends(get_current_active_user)):
        if current_user.role not in role:
            raise HTTPException(detail=f"Role required: {role}, user is {current_user.role}", status_code=status.HTTP_403_FORBIDDEN)
        return current_user
    return role_checker


# require_admin = required_role("admin")
# require_staff = required_role("admin", "moderator")

