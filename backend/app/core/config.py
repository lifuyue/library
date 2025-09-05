import os
from typing import List

class Settings:
    # JWT 配置
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    # 数据库配置（仅支持 PostgreSQL）
    # 必须通过环境变量 DATABASE_URL 提供，格式：
    # 同步: postgresql+psycopg://USER:PASSWORD@HOST:5432/DBNAME
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    # CORS配置
    CORS_ORIGINS: List[str] = os.getenv(
        "CORS_ORIGINS", 
        "http://localhost:3000,http://127.0.0.1:3000"
    ).split(",")

    # 文件上传配置
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", str(50 * 1024 * 1024)))  # 50MB
    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mov', '.avi', '.webm'}
    
    # 服务器配置
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # 环境配置
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # 默认管理员（若数据库中不存在任何管理员账号会自动创建）
    ADMIN_DEFAULT_USERNAME: str = os.getenv("ADMIN_DEFAULT_USERNAME", "admin")
    ADMIN_DEFAULT_EMAIL: str = os.getenv("ADMIN_DEFAULT_EMAIL", "admin@example.com")
    ADMIN_DEFAULT_PASSWORD: str = os.getenv("ADMIN_DEFAULT_PASSWORD", "admin123")

settings = Settings()

if not settings.DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is required")

# 向后兼容的常量
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
DATABASE_URL = settings.DATABASE_URL
UPLOAD_DIR = settings.UPLOAD_DIR
MAX_FILE_SIZE = settings.MAX_FILE_SIZE
ALLOWED_EXTENSIONS = settings.ALLOWED_EXTENSIONS
ADMIN_DEFAULT_USERNAME = settings.ADMIN_DEFAULT_USERNAME
ADMIN_DEFAULT_EMAIL = settings.ADMIN_DEFAULT_EMAIL
ADMIN_DEFAULT_PASSWORD = settings.ADMIN_DEFAULT_PASSWORD
