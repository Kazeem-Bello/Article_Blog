from fastapi import APIRouter, status, HTTPException, Depends
from repositories.user_repo import UserRepository
from schemas.user_schema import UserCreate, UserPublic, UserUpdate
from db.deps import get_db
from sqlalchemy.orm import Session
from typing import List


user_router = APIRouter()


@user_router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserPublic)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    user = UserRepository.create_user(user_in=user_in, db=db)
    return user


@user_router.get("/", status_code=status.HTTP_200_OK, response_model=List[UserPublic])
def retrieve_users(db: Session = Depends(get_db)):
    users = UserRepository.retrieve_users(db=db)
    return users


# @user_router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserPublic)
# def get_user_by_id(id: int, db: Session = Depends(get_db)):
#     user = UserRepository.get_user_by_id(id=id, db=db)
#     if not user:
#         raise HTTPException(detail=f"user with id {id} not found", status_code=status.HTTP_404_NOT_FOUND)
#     return user


@user_router.get("/{email}", status_code=status.HTTP_200_OK, response_model=UserPublic)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = UserRepository.get_by_email(email=email, db=db)
    if not user:
        raise HTTPException(detail="user not found", status_code=status.HTTP_404_NOT_FOUND)
    return user


@user_router.put("/{id}", status_code=status.HTTP_200_OK, response_model=UserPublic)
def update_user(id: int, user_in: UserUpdate, db: Session = Depends(get_db)):
    user = UserRepository.update_user(id=id, user_in=user_in, db=db)
    if not user:
        raise HTTPException(detail="user not found", status_code=status.HTTP_404_NOT_FOUND)
    db.commit()
    return user


@user_router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_user(id: int, db: Session = Depends(get_db)):
    return UserRepository.delete_user(id=id, db=db)