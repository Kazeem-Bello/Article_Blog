from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    email: EmailStr
    password: str
    
    # model_config = ConfigDict(from_attributes=True)

    
# class User(UserBase):
#     id: int
#     is_active: bool
    
class UserCreate(UserBase):
    pass

class UserPublic(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    
class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None