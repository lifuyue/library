import os
import re
import sys
import time

from dotenv import load_dotenv
from pathlib import Path
import psycopg


def normalize_db_url(url: str) -> str:
    """Normalize SQLAlchemy-style 'postgresql+driver://' URLs to plain 'postgresql://' for psycopg.

    Examples:
        postgresql+psycopg://user:pass@host:5432/db -> postgresql://user:pass@host:5432/db
        postgresql+asyncpg://u:p@h/db -> postgresql://u:p@h/db
    If it already matches plain postgresql:// it is returned unchanged.
    """
    if not url:
        return url
    # Replace leading 'postgresql+<driver>://' with 'postgresql://'
    return re.sub(r'^postgresql\+[^:]+://', 'postgresql://', url, count=1)


def main():
    # Load .env from default location and explicitly from /app/.env when running in container
    load_dotenv()
    app_env = Path('/app/.env')
    if app_env.exists():
        load_dotenv(dotenv_path=app_env)
    database_url_raw = os.getenv("DATABASE_URL")
    if not database_url_raw:
        print("[wait_for_db] DATABASE_URL is not set; please define it in the environment or .env file")
        sys.exit(1)

    db_url = normalize_db_url(database_url_raw)
    timeout = int(os.getenv("DB_WAIT_TIMEOUT", "30"))

    start = time.time()
    while True:
        try:
            with psycopg.connect(db_url) as conn:
                conn.execute("SELECT 1")
            print("[wait_for_db] database is ready")
            break
        except Exception as e:
            elapsed = time.time() - start
            if elapsed > timeout:
                raise RuntimeError(f"Database not ready: {e}")
            print(f"[wait_for_db] waiting for database... {e}")
            time.sleep(1)


if __name__ == "__main__":
    main()
