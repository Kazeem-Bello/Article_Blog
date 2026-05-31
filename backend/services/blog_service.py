from fastapi import HTTPException, status, Depends  
from models.blog_model import Blog
from schemas.blog_schema import BlogCreate, BlogPublic, BlogUpdate
from sqlalchemy.orm import Session
from repositories.blog_repo import BlogRepository


class BlogService:
    
    @staticmethod
    def create_blog(blog_in: BlogCreate, db: Session, author_id: int):
        blog = BlogRepository.create_blog(blog_in=blog_in, db=db, author_id=author_id)
        db.commit()
        return blog
    
    
    @staticmethod
    def retrieve_blogs(db: Session):
        blogs = BlogRepository.retrieve_blogs(db=db)
        return blogs
    
    
    @staticmethod
    def get_by_id(id: int, db: Session):
        blog = BlogRepository.get_by_id(id=id, db=db)
        if not blog:
            raise HTTPException(detail="Blog not found", status_code=status.HTTP_404_NOT_FOUND)
        return blog
    
    
    @staticmethod
    def update_blog(id: int, blog_in: BlogUpdate, db: Session):
        blog = BlogRepository.update_blog(id=id, blog_in=blog_in, db=db)
        if not blog:
            raise HTTPException(detail="Blog not found", status_code=status.HTTP_404_NOT_FOUND)
        db.commit()
        return blog
        
        
    @staticmethod
    def delete_blog(id: int, db):
        return BlogRepository.delete_blog(id=id, db=db)
        
    