from typing import Optional
from unittest.util import strclass
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
# We are going to define a class
class PostBase(BaseModel):
  title:str
  content:str
  # can provide a default value
  published:bool = True 
  # fully Optional field (wathc should use semicolumn)
  # rating: Optional[int] = None

class PostCreate(PostBase): 
  pass # will inherit all the columns form PostBase

# why here? because in Post Response class we reference it 
class UserResponse(BaseModel): 
  id:int
  email:EmailStr
  created_at:datetime
  class Config: 
    orm_mode=True

class PostResponse(PostBase): 
  id:int
  created_at:datetime
  owner_id: int
  owner: UserResponse
  # it is very important, because when we use sqlalchemy it will return sqlalchemy model and 
  # fastapi should convert orm model to pydantic model
  class Config: 
    orm_mode=True
  
class PostVote(BaseModel): 
  Post: PostResponse
  votes: int
  class Config: 
    orm_mode=True
  
class UserCreate(BaseModel): 
  email: EmailStr
  password: str

class UserLogin(BaseModel): 
  email:EmailStr
  password: str

class Token(BaseModel): 
  access_token: str
  token_type: str

class TokenData(BaseModel): 
  id: Optional [str] = None

class Vote(BaseModel): 
  post_id: int
  dir: conint(le=1)