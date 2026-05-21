from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from db.deps import get_db
from repositories.blog_repo import BlogRepository
from schemas.blog_schema import BlogCreate, BlogPublic, BlogUpdate
from typing import List




blog_router = APIRouter()


@blog_router.post("/", status_code=status.HTTP_201_CREATED, response_model=BlogPublic)
def create_blog(
    blog_in: BlogCreate, 
    db: Session = Depends(get_db)
):
    blog = BlogRepository.create_blog(blog_in=blog_in, db=db)
    return blog    


@blog_router.get("/", status_code=status.HTTP_200_OK, response_model=List[BlogPublic])
def retrieve_blogs(db: Session = Depends(get_db)):
    blogs = BlogRepository.retrieve_blogs(db=db)
    return blogs


@blog_router.put("/{id}", status_code=status.HTTP_200_OK, response_model=BlogPublic)
def update_blog(id: int, blog_in: BlogUpdate, db: Session = Depends(get_db)):
    blog = BlogRepository.update_blog(id=id, blog_in=blog_in, db=db)
    if not blog:
        raise HTTPException(detail=f"Blog not found", status_code=status.HTTP_404_NOT_FOUND)
    return blog


@blog_router.get("/{id}", status_code=status.HTTP_200_OK, response_model=BlogPublic)
def get_blog_by_id(id: int, db: Session = Depends(get_db)):
    blog = BlogRepository.get_blog_by_id(id=id, db=db)
    if not blog:
        raise HTTPException(detail=f"Blog not found", status_code=status.HTTP_404_NOT_FOUND)
    return blog


@blog_router.delete("/", status_code=status.HTTP_200_OK)
def delete_blog(id: int, db: Session = Depends(get_db)):
    return BlogRepository.delete_blog(id=id, db=db)