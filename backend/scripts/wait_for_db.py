import os
import re
import time
import psycopg

DATABASE_URL_RAW = os.getenv("DATABASE_URL")
TIMEOUT = int(os.getenv("DB_WAIT_TIMEOUT", "30"))  # seconds


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
    if not DATABASE_URL_RAW:
        raise RuntimeError("DATABASE_URL is not set")

    db_url = normalize_db_url(DATABASE_URL_RAW)

    start = time.time()
    while True:
        try:
            with psycopg.connect(db_url) as conn:
                conn.execute("SELECT 1")
            print("[wait_for_db] database is ready")
            break
        except Exception as e:
            elapsed = time.time() - start
            if elapsed > TIMEOUT:
                raise RuntimeError(f"Database not ready: {e}")
            print(f"[wait_for_db] waiting for database... {e}")
            time.sleep(1)


if __name__ == "__main__":
    main()
