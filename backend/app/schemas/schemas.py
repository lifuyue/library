from pydantic import BaseModel, EmailStr, ConfigDict
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
    is_admin: bool = False
    created_at: datetime

    # Pydantic v2 配置
    model_config = ConfigDict(from_attributes=True)

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

    model_config = ConfigDict(from_attributes=True)

class MaterialResponse(BaseModel):
    materials: List[Material]
    total: int
    page: int
    size: int

    model_config = ConfigDict(from_attributes=True)

# 管理员相关 Schema
class AdminStats(BaseModel):
    total_materials: int
    approved_materials: int
    pending_materials: int
    total_users: int
    active_users: int

class AdminUser(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    is_admin: bool
    created_at: datetime
    materials_count: int

    model_config = ConfigDict(from_attributes=True)

class MaterialAction(BaseModel):
    action: str  # "approve" or "reject"
    reason: Optional[str] = None
