from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

"""数据库初始化（PostgreSQL only）

要求：环境变量 DATABASE_URL 必须存在，格式：
  postgresql+psycopg2://USER:PASSWORD@HOST:5432/DBNAME
不再支持 SQLite，移除所有相关兼容逻辑。
"""

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL.strip()

# Allow developers to omit the driver in DATABASE_URL. If a plain
# ``postgresql://`` URL is provided, automatically upgrade it to the
# required ``postgresql+psycopg2://`` form so the application can start
# without manual tweaks.
if SQLALCHEMY_DATABASE_URL.startswith("postgresql://") and "+" not in SQLALCHEMY_DATABASE_URL.split("//", 1)[1]:
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace(
        "postgresql://", "postgresql+psycopg2://", 1
    )

if not SQLALCHEMY_DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is required (e.g., postgresql+psycopg2://user:pass@host:5432/db)"
    )

url_obj = make_url(SQLALCHEMY_DATABASE_URL)
if url_obj.drivername != "postgresql+psycopg2":
    raise RuntimeError("DATABASE_URL must use postgresql+psycopg2")

engine = create_engine(url_obj, pool_pre_ping=True, future=True)

safe_url = url_obj.render_as_string(hide_password=True)
print(f"[DB INIT] URL={safe_url}")

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

# FastAPI 依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
