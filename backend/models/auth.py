from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
    
class TokenData(BaseModel):      #decode JWT payload
    username: str | None = None
    role: str | None = None