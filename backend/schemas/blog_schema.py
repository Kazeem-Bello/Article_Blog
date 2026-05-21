from pydantic import BaseModel, Field, model_validator
from datetime import datetime


class BlogBase(BaseModel):
    title: str
    slug: str
    content: str | None = None
    
    @model_validator(mode="before")
    @classmethod
    def generate_slug(cls, values):
        if "title" in values:
            values["slug"] = "-".join(values["title"].lower().split())
        return values
   
   
class Blog(BlogBase):
    id: int
    created_at: datetime
    author_id: int
    
class BlogCreate(BlogBase):
    pass


class BlogPublic(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    
    
class BlogUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
