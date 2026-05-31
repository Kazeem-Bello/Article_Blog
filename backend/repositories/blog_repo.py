from models.blog_model import Blog
from schemas.blog_schema import BlogCreate, BlogPublic, BlogUpdate
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from fastapi import HTTPException, status


class BlogRepository:
    """All database blog operations"""
    
    @staticmethod
    def create_blog(blog_in: BlogCreate, db: Session, author_id: int) -> Blog:
        blog = Blog(
            title = blog_in.title,
            slug = blog_in.slug,
            content= blog_in.content,
            author_id=author_id
        )
        db.add(blog)
        db.flush()
        db.refresh(blog)
        return blog 
    
    
    @staticmethod
    def retrieve_blogs(db: Session):
        blogs = db.scalars(select(Blog)).all()
        return blogs
    
    
    @staticmethod
    def get_by_id(id: int, db: Session):
        blog = db.scalars(select(Blog).where(Blog.id == id)).first()
        return blog
    
    
    @staticmethod
    def update_blog(id:int, blog_in: BlogUpdate, db: Session):
        blog = db.get(Blog, id)
        blog_data = blog_in.model_dump(exclude_unset=True)
        if "title" in blog_data:
            blog_data["slug"] = "-".join(blog_data["title"].lower().split())
        for key, value in blog_data.items():
            setattr(blog, key, value)
        db.add(blog)
        db.flush()
        db.refresh(blog)
        return blog
    
    
    @staticmethod
    def delete_blog(id: int, db: Session):
        blog = db.get(Blog, id)
        if not blog:
            raise HTTPException(detail="Blog not found", status_code=status.HTTP_404_NOT_FOUND)
        db.delete(blog)
        db.commit()
        return {"message": "Blog Deleted"}
        
        
        