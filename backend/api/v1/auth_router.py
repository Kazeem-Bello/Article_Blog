from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from services.auth_services import AuthServices
from db.deps import get_current_active_user, get_db, get_current_user
from schemas.auth import Token
from schemas.user_schema import UserCreate, UserPublic, UserLogin
from models.user_model import User
from sqlalchemy.orm import Session


auth_router = APIRouter()


@auth_router.post("/register", response_model=UserPublic)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    return AuthServices.register(user_in=user_in, db=db)


# @auth_router.post("/token", response_model=Token)
# def login(form_data: UserLogin, db: Session = Depends(get_db)):
#     return AuthServices.login(username_or_email=form_data.email, password=form_data.password, db=db)


@auth_router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return AuthServices.login(username_or_email=form_data.username, password=form_data.password, db=db)


@auth_router.post("/me", response_model=UserPublic)
def me(current_user = Depends(get_current_active_user)):
    return current_user

@auth_router.post("/refresh-token")
def refresh_token(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("refresh_token")
    return AuthServices.refresh_token(token=token, db=db)

@auth_router.post("/send-email-verification")
def send_email_verification(user: User = Depends(get_current_active_user)):
    return AuthServices.send_email_verification_token(user=user)

@auth_router.post("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    return AuthServices.verify_email(token=token, db=db)