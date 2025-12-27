from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    full_name: str
    role: str

    class Config:
        from_attributes = True


#ADMIN

class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str
    role: str  # admin / manager / staff


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[str] = None