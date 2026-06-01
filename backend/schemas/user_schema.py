from pydantic import BaseModel, EmailStr, Field, ConfigDict,field_validator
import re

class UserBase(BaseModel):
    email: EmailStr
    password: str
    username: str
    
    # @field_validator("password")
    # @classmethod
    # def validate_password(cls, password: str):
    #     pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{5,}$"
        
    #     if not re.match(pattern, password):
    #         raise ValueError(
    #             "Password must be at least 8 characters long and contain one uppercase letter, "
    #             "one lowercase letter, one number, and one special character"
    #         )
    #     return password
            
        
   
    # model_config = ConfigDict(from_attributes=True)

    
class UserLogin(BaseModel):
    email: str
    password: str
    
class UserCreate(UserBase):
    pass

class UserPublic(BaseModel):
    id: int
    email: EmailStr
    username: str

    
class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None