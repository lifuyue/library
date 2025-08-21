from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path

# 统一使用 backend 根目录下的 materials.db，避免因工作目录不同产生多个副本
BASE_DIR = Path(__file__).resolve().parents[2]  # backend 目录
DB_FILE = BASE_DIR / "materials.db"
# 使用正斜杠防止 Windows 反斜杠带来解析问题
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_FILE.as_posix()}"  # 绝对路径

print(f"[DB INIT] Using SQLite DB at: {DB_FILE}")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

from app.core.config import (
    ADMIN_DEFAULT_USERNAME,
    ADMIN_DEFAULT_EMAIL,
    ADMIN_DEFAULT_PASSWORD,
)
from sqlalchemy.orm import Session

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def _ensure_schema():
    """在无迁移系统情况下，确保关键新增列存在 (轻量级解决方案)。
    目前只处理 users.is_admin 缺失问题，避免旧库报错。
    SQLite 限制下简单 ALTER。"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("PRAGMA table_info(users)"))
            columns = [row[1] for row in result.fetchall()]  # PRAGMA table_info 返回 (cid, name, ...)
            if "is_admin" not in columns:
                print("[DB MIGRATION] Adding missing column users.is_admin ...")
                conn.execute(text("ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT 0"))
                conn.commit()
                print("[DB MIGRATION] users.is_admin added.")
    except Exception as e:
        # 打印但不阻断应用启动
        print(f"[DB MIGRATION][WARN] Auto schema ensure failed: {e}")

# 立即执行一次（在模型 create_all 之前 / 之后都可以，此处放在定义阶段）
# NOTE: 自动 schema 修补已迁移到 Alembic migrations，移除运行时自动修改
# _ensure_schema()

# NOTE: 管理员自动创建已迁移到 Alembic migrations，移除运行时自动创建
# def ensure_default_admin():
#     """管理员创建逻辑已迁移到 Alembic migration 8d300e45b937_add_is_admin_column_and_seed_admin.py
#     请使用: alembic upgrade head 来应用数据库迁移和创建默认管理员
#     """
#     pass

# 数据库依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
