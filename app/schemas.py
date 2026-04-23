from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime

from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

class PostCreate(PostBase):
    pass

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    created_at: datetime

class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    
    # class Config:
    #     orm_mode = True

class PostOut(BaseModel):
     model_config = ConfigDict(from_attributes=True)
     Post: PostResponse
     votes: int

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int]
    
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)