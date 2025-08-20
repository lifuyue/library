from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import uuid
from pathlib import Path
from PIL import Image
import aiofiles

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models import models
from app.schemas import schemas

router = APIRouter()

# 允许的文件类型
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mov', '.avi', '.webm'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

def get_file_extension(filename: str) -> str:
    return os.path.splitext(filename)[1].lower()

def is_allowed_file(filename: str) -> bool:
    return get_file_extension(filename) in ALLOWED_EXTENSIONS

def get_file_type(filename: str) -> str:
    ext = get_file_extension(filename)
    if ext in ['.jpg', '.jpeg', '.png']:
        return 'image'
    elif ext == '.gif':
        return 'gif'
    elif ext in ['.mp4', '.mov', '.avi', '.webm']:
        return 'video'
    return 'unknown'

@router.get("/", response_model=schemas.MaterialResponse)
async def get_materials(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    category: Optional[str] = Query(None),
    map_name: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """获取素材列表"""
    skip = (page - 1) * size
    
    query = db.query(models.Material).filter(models.Material.is_approved == True)
    
    if category:
        query = query.filter(models.Material.category == category)
    if map_name:
        query = query.filter(models.Material.map_name == map_name)
    if search:
        query = query.filter(
            models.Material.title.contains(search) |
            models.Material.description.contains(search) |
            models.Material.tags.contains(search)
        )
    
    total = query.count()
    materials = query.offset(skip).limit(size).all()
    
    return schemas.MaterialResponse(
        materials=materials,
        total=total,
        page=page,
        size=size
    )

@router.get("/{material_id}", response_model=schemas.Material)
async def get_material(material_id: int, db: Session = Depends(get_db)):
    """获取单个素材详情"""
    material = db.query(models.Material).filter(models.Material.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="素材不存在")
    
    # 增加浏览次数
    material.views += 1
    db.commit()
    
    return material

@router.post("/upload", response_model=schemas.Material)
async def upload_material(
    title: str,
    category: str,
    description: Optional[str] = None,
    map_name: Optional[str] = None,
    tags: Optional[str] = None,
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """上传素材文件"""
    
    # 验证文件类型
    if not is_allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="不支持的文件类型")
    
    # 读取文件内容以确定大小
    content = await file.read()
    file_size = len(content)
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="文件大小超出限制")
    # 回到开头供后续保存
    # (我们已在 content 中持有数据, 不再依赖 file.read())
    
    # 生成唯一文件名
    file_ext = get_file_extension(file.filename)
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    # 与 main.py 中的 UPLOAD_DIR 保持一致
    base_dir = Path(__file__).resolve().parents[2]  # 到 backend 目录
    upload_dir = base_dir / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)
    relative_name = unique_filename
    file_path = upload_dir / relative_name
    
    # 确保上传目录存在
    os.makedirs("uploads", exist_ok=True)
    
    # 保存文件
    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(content)
    
    # 生成缩略图（仅对图片）
    thumbnail_path = None
    file_type = get_file_type(file.filename)
    if file_type == 'image':
        try:
            thumbnail_filename = f"thumb_{unique_filename}"
            thumb_path_obj = upload_dir / thumbnail_filename
            thumbnail_path = str(thumb_path_obj)
            
            with Image.open(file_path) as img:
                img.thumbnail((300, 300))
                img.save(thumbnail_path, optimize=True, quality=85)
        except Exception as e:
            print(f"生成缩略图失败: {e}")
    
    # 创建数据库记录
    material = models.Material(
        title=title,
        description=description,
        category=category,
        map_name=map_name,
    file_path=relative_name,
        file_type=file_type,
    file_size=file_size,
    thumbnail_path=thumbnail_path if thumbnail_path else None,
        tags=tags,
        uploader_id=current_user.id,  # 使用当前登录用户
        is_approved=True  # 暂时自动审核通过
    )
    
    db.add(material)
    db.commit()
    db.refresh(material)
    
    return material

@router.post("/{material_id}/like")
async def like_material(material_id: int, db: Session = Depends(get_db)):
    material = db.query(models.Material).filter(models.Material.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="素材不存在")
    material.likes += 1
    db.commit()
    return {"likes": material.likes}

@router.get("/categories/list")
async def get_categories():
    """获取道具类别列表"""
    return {
        "categories": [
            {"value": "smoke", "label": "烟雾弹"},
            {"value": "flash", "label": "闪光弹"},  
            {"value": "he", "label": "手雷"},
            {"value": "molotov", "label": "燃烧瓶"},
            {"value": "position", "label": "身位点位"},
            {"value": "strategy", "label": "战术策略"},
            {"value": "other", "label": "其他"}
        ]
    }

@router.get("/maps/list")
async def get_maps():
    """获取地图列表"""
    return {
        "maps": [
            "dust2", "mirage", "inferno", "cache", "overpass",
            "train", "cobblestone", "nuke", "vertigo", "ancient"
        ]
    }
