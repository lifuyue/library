from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from app.core.config import settings

"""数据库初始化逻辑

改进点:
1. 不再硬编码为 SQLite, 统一使用环境变量 settings.DATABASE_URL
2. 若是 SQLite 相对路径 -> 转换为项目根下绝对路径, 避免因工作目录不同生成多个副本
3. 兼容 Postgres / 其它 SQLAlchemy URL (无需额外 connect_args)
4. 暴露 DB_FILE (仅对 SQLite 生效, 供 / 根路由调试显示)
"""

RAW_DATABASE_URL = settings.DATABASE_URL
DB_FILE = None  # 仅在使用 SQLite 文件时赋值

def _normalize_sqlite_url(url: str) -> str:
    if not url.startswith("sqlite"):
        return url
    # 形如 sqlite:///materials.db 或 sqlite:///./cs_library.db
    prefix = "sqlite:///"
    if url.startswith(prefix):
        path_part = url[len(prefix):]
        # 内存数据库 / URI 形式不改
        if path_part in (":memory:", "") or path_part.startswith("/"):
            return url  # 已是绝对路径或内存
        # 相对路径 -> 放置到 backend 根目录(当前文件的上两级目录)
        base_dir = Path(__file__).resolve().parents[2]
        abs_path = (base_dir / path_part).resolve()
        return f"sqlite:///{abs_path.as_posix()}"
    return url

SQLALCHEMY_DATABASE_URL = _normalize_sqlite_url(RAW_DATABASE_URL)

if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    # 提取文件路径用于调试显示
    try:
        path_part = SQLALCHEMY_DATABASE_URL.replace("sqlite:///", "", 1)
        if path_part not in (":memory:", ""):
            # 绝对路径
            DB_FILE = Path(path_part)
    except Exception:
        DB_FILE = None

connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)

print(f"[DB INIT] URL={SQLALCHEMY_DATABASE_URL}")
if DB_FILE:
    print(f"[DB INIT] SQLite file: {DB_FILE}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI 依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
