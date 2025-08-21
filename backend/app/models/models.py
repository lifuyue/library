from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)  # 是否为管理员
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关联素材
    materials = relationship("Material", back_populates="uploader")

class Material(Base):
    __tablename__ = "materials"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    category = Column(String(50), nullable=False)  # 道具类别: smoke, flash, he, molotov 等
    map_name = Column(String(50))  # 地图名称
    file_path = Column(String(500), nullable=False)  # 文件路径
    file_type = Column(String(20), nullable=False)  # 文件类型: image, video, gif
    file_size = Column(Integer)  # 文件大小(字节)
    thumbnail_path = Column(String(500))  # 缩略图路径
    tags = Column(Text)  # 标签，用逗号分隔
    views = Column(Integer, default=0)  # 浏览次数
    likes = Column(Integer, default=0)  # 点赞数
    uploader_id = Column(Integer, ForeignKey("users.id"))
    is_approved = Column(Boolean, default=False)  # 是否审核通过
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联用户
    uploader = relationship("User", back_populates="materials")
