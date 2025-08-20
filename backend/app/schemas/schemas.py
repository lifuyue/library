from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# 用户相关 Schema
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

# 素材相关 Schema  
class MaterialBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    map_name: Optional[str] = None
    tags: Optional[str] = None

class MaterialCreate(MaterialBase):
    pass

class Material(MaterialBase):
    id: int
    file_path: str
    file_type: str
    file_size: Optional[int] = None
    thumbnail_path: Optional[str] = None
    views: int = 0
    likes: int = 0
    uploader_id: int
    is_approved: bool = False
    created_at: datetime
    updated_at: datetime
    uploader: User
    
    class Config:
        orm_mode = True

class MaterialResponse(BaseModel):
    materials: List[Material]
    total: int
    page: int
    size: int
