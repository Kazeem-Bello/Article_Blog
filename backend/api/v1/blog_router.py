from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from db.deps import get_db
from services.blog_service import BlogService
from schemas.blog_schema import BlogCreate, BlogPublic, BlogUpdate
from typing import List
from db.deps import get_current_active_user
from models.user_model import User




blog_router = APIRouter()


@blog_router.post("/", status_code=status.HTTP_201_CREATED, response_model=BlogPublic)
def create_blog(
    blog_in: BlogCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return BlogService.create_blog(blog_in=blog_in, db=db, author_id=current_user.id) 


@blog_router.get("/", status_code=status.HTTP_200_OK, response_model=List[BlogPublic])
def retrieve_blogs(db: Session = Depends(get_db)):
    return BlogService.retrieve_blogs(db=db)


@blog_router.put("/{id}", status_code=status.HTTP_200_OK, response_model=BlogPublic)
def update_blog(id: int, blog_in: BlogUpdate, db: Session = Depends(get_db)):
    return BlogService.update_blog(id=id, blog_in=blog_in, db=db)


@blog_router.get("/{id}", status_code=status.HTTP_200_OK, response_model=BlogPublic)
def get_by_id(id: int, db: Session = Depends(get_db)):
    return BlogService.get_by_id(id=id, db=db)
  

@blog_router.delete("/", status_code=status.HTTP_200_OK)
def delete_blog(id: int, db: Session = Depends(get_db)):
    return BlogService.delete_blog(id=id, db=db)