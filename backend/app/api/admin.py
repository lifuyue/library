from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
import os

from app.core.database import get_db
from app.core.auth import get_admin_user
from app.models import models
from app.schemas import schemas

router = APIRouter()

@router.get("/stats", response_model=schemas.AdminStats)
async def get_admin_stats(
    admin_user: models.User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """获取管理员统计信息"""
    total_materials = db.query(models.Material).count()
    approved_materials = db.query(models.Material).filter(models.Material.is_approved == True).count()
    pending_materials = total_materials - approved_materials
    
    total_users = db.query(models.User).count()
    active_users = db.query(models.User).filter(models.User.is_active == True).count()
    
    return schemas.AdminStats(
        total_materials=total_materials,
        approved_materials=approved_materials,
        pending_materials=pending_materials,
        total_users=total_users,
        active_users=active_users
    )

@router.get("/materials/pending", response_model=schemas.MaterialResponse)
async def get_pending_materials(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    admin_user: models.User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """获取待审核素材列表"""
    skip = (page - 1) * size
    
    query = db.query(models.Material).filter(models.Material.is_approved == False)
    total = query.count()
    
    materials = query.order_by(models.Material.created_at.desc()).offset(skip).limit(size).all()
    
    return schemas.MaterialResponse(
        materials=materials,
        total=total,
        page=page,
        size=size
    )

@router.post("/materials/{material_id}/approve")
async def approve_material(
    material_id: int,
    admin_user: models.User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """审核通过素材"""
    material = db.query(models.Material).filter(models.Material.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="素材不存在")
    
    material.is_approved = True
    db.commit()
    
    return {"message": "素材审核通过"}

@router.post("/materials/{material_id}/reject")
async def reject_material(
    material_id: int,
    admin_user: models.User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """拒绝素材"""
    material = db.query(models.Material).filter(models.Material.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="素材不存在")
    
    # 删除文件
    if material.file_path:
        file_path = f"uploads/{material.file_path}"
        if os.path.exists(file_path):
            os.remove(file_path)
    
    if material.thumbnail_path:
        thumb_path = f"uploads/{material.thumbnail_path}"
        if os.path.exists(thumb_path):
            os.remove(thumb_path)
    
    # 删除数据库记录
    db.delete(material)
    db.commit()
    
    return {"message": "素材已拒绝并删除"}

@router.delete("/materials/{material_id}")
async def delete_material(
    material_id: int,
    admin_user: models.User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """删除素材"""
    material = db.query(models.Material).filter(models.Material.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="素材不存在")
    
    # 删除文件
    if material.file_path:
        file_path = f"uploads/{material.file_path}"
        if os.path.exists(file_path):
            os.remove(file_path)
    
    if material.thumbnail_path:
        thumb_path = f"uploads/{material.thumbnail_path}"
        if os.path.exists(thumb_path):
            os.remove(thumb_path)
    
    # 删除数据库记录
    db.delete(material)
    db.commit()
    
    return {"message": "素材已删除"}

@router.get("/users", response_model=List[schemas.AdminUser])
async def get_users(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    admin_user: models.User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """获取用户列表"""
    skip = (page - 1) * size
    
    # 查询用户及其素材数量
    users_with_counts = db.query(
        models.User,
        func.count(models.Material.id).label('materials_count')
    ).outerjoin(models.Material).group_by(models.User.id).offset(skip).limit(size).all()
    
    result = []
    for user, materials_count in users_with_counts:
        admin_user_data = schemas.AdminUser(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            is_admin=user.is_admin,
            created_at=user.created_at,
            materials_count=materials_count
        )
        result.append(admin_user_data)
    
    return result

@router.post("/users/{user_id}/toggle-active")
async def toggle_user_active(
    user_id: int,
    admin_user: models.User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """切换用户激活状态"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    if user.id == admin_user.id:
        raise HTTPException(status_code=400, detail="不能修改自己的状态")
    
    user.is_active = not user.is_active
    db.commit()
    
    return {"message": f"用户已{'激活' if user.is_active else '禁用'}"}

@router.post("/users/{user_id}/toggle-admin")
async def toggle_user_admin(
    user_id: int,
    admin_user: models.User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """切换用户管理员状态"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    if user.id == admin_user.id:
        raise HTTPException(status_code=400, detail="不能修改自己的管理员权限")
    
    user.is_admin = not user.is_admin
    db.commit()
    
    return {"message": f"用户已{'设为' if user.is_admin else '取消'}管理员"}
