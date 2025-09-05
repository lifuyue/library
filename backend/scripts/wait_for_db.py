import os
import time
import psycopg

DATABASE_URL = os.getenv("DATABASE_URL")
TIMEOUT = int(os.getenv("DB_WAIT_TIMEOUT", "30"))

def main():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set")
    start = time.time()
    while True:
        try:
            with psycopg.connect(DATABASE_URL) as conn:
                conn.execute("SELECT 1")
            break
        except Exception as e:
            if time.time() - start > TIMEOUT:
                raise RuntimeError(f"Database not ready: {e}")
            print("[wait_for_db] waiting for database...", str(e))
            time.sleep(1)

if __name__ == "__main__":
    main()
