#!/bin/sh
set -ex

echo "[pg-entrypoint] Starting PostgreSQL with verbose logging"
echo "[pg-entrypoint] Effective UID: $(id -u), GID: $(id -g)"
echo "[pg-entrypoint] POSTGRES_DB=${POSTGRES_DB:-} POSTGRES_USER=${POSTGRES_USER:-}"

# Chain to the original docker entrypoint with explicit postgres command and logging flags
exec /usr/local/bin/docker-entrypoint.sh postgres \
  -c log_destination=stderr \
  -c logging_collector=off \
  -c log_min_messages=debug1 \
  -c log_statement=all \
  -c client_min_messages=log \
  "$@"
