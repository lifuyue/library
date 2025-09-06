#!/bin/bash
set -e

echo "[entrypoint] loading env from /app/.env if present"
if [ -f /app/.env ]; then
	set -a
	. /app/.env
	set +a
fi

echo "[entrypoint] DATABASE_URL=$DATABASE_URL"

python /app/scripts/wait_for_db.py

alembic upgrade head

exec "$@"
