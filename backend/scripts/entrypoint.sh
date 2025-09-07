#!/bin/bash
set -euo pipefail
set -x

echo "[entrypoint] loading env from /app/.env if present"
if [ -f /app/.env ]; then
	set -a
	. /app/.env
	set +a
fi

echo "[entrypoint] DATABASE_URL=${DATABASE_URL:-}"
echo "[entrypoint] ENVIRONMENT=${ENVIRONMENT:-} HOST=${HOST:-} PORT=${PORT:-}"
echo "[entrypoint] python: $(python --version)"
echo "[entrypoint] working dir: $(pwd)"
echo "[entrypoint] listing /app:"
ls -la /app || true

PYTHONFAULTHANDLER=1 python -X faulthandler /app/scripts/wait_for_db.py

alembic upgrade head

exec "$@"
