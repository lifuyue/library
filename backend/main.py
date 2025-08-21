from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import os
from pathlib import Path
from datetime import datetime

from app.core.database import get_db, engine, DB_FILE
from app.models import models
from app.schemas import schemas
from app.api import materials, users
from app.core.config import settings

# 创建数据库表
# NOTE: 管理员创建和 schema 修补现在通过 Alembic migrations 处理
# 运行 'alembic upgrade head' 来应用迁移和创建默认管理员
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CS素材库 API",
    description="反恐精英道具教程素材集 API",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件服务（使用绝对路径，避免启动目录差异）
BASE_DIR = Path(__file__).resolve().parent  # backend 目录
UPLOAD_DIR = BASE_DIR / settings.UPLOAD_DIR
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

# API 路由
app.include_router(materials.router, prefix="/api/materials", tags=["materials"])
app.include_router(users.router, prefix="/api/users", tags=["users"])

# 导入管理员路由
from app.api import admin
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])

@app.get("/")
async def root():
    return {
        "message": "CS素材库 API 服务正在运行",
        "environment": settings.ENVIRONMENT,
    "version": "1.0.0",
    "database_path": str(DB_FILE)
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=settings.HOST, 
        port=settings.PORT,
        reload=(settings.ENVIRONMENT == "development")
    )
