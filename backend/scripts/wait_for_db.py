import logging
import os
import re
import sys
import time
import socket

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
    logging.basicConfig(level=logging.INFO, format="[wait_for_db] %(message)s")
    logger = logging.getLogger(__name__)

    # Load .env from default location and explicitly from /app/.env when running in container
    load_dotenv()
    app_env = Path('/app/.env')
    if app_env.exists():
        logger.info(f"loading env from {app_env}")
        load_dotenv(dotenv_path=app_env)

    database_url_raw = os.getenv("DATABASE_URL")
    logger.info(f"raw DATABASE_URL: {database_url_raw}")
    if not database_url_raw:
        logger.error("DATABASE_URL is not set; please define it in the environment or .env file")
        sys.exit(1)

    db_url = normalize_db_url(database_url_raw)
    logger.info(f"normalized DB URL: {db_url}")
    # Parse host for DNS diagnostics
    host = None
    try:
        m = re.match(r"^postgresql://[^@]+@([^/:]+)", db_url)
        host = m.group(1) if m else None
    except Exception:
        host = None
    if host:
        logger.info(f"parsed host: {host}")
        try:
            addrs = socket.getaddrinfo(host, 5432, proto=socket.IPPROTO_TCP)
            ips = sorted({a[4][0] for a in addrs})
            logger.info(f"DNS {host} -> {ips}")
        except Exception as e:
            logger.info(f"DNS resolve failed for {host}: {e}")
    timeout = int(os.getenv("DB_WAIT_TIMEOUT", "30"))

    start = time.time()
    while True:
        try:
            with psycopg.connect(db_url) as conn:
                conn.execute("SELECT 1")
            logger.info("database is ready")
            break
        except Exception as e:
            elapsed = time.time() - start
            if elapsed > timeout:
                raise RuntimeError(f"Database not ready: {e}")
            logger.info(f"waiting for database... {type(e).__name__}: {e} (elapsed {int(elapsed)}s)")
            time.sleep(1)


if __name__ == "__main__":
    main()
