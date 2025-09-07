# Production Deployment (PostgreSQL)

This guide explains how to run the stack (FastAPI + Vue + PostgreSQL) using `docker-compose.prod.yml`.

## Files
```
deploy/docker/
  Dockerfile.backend
  Dockerfile.frontend
  nginx.conf
  .env.postgres
  docker-compose.prod.yml
```

## 1. Prepare environment
Edit `.env.postgres` and change:
- SECRET_KEY
- POSTGRES_PASSWORD
- ADMIN_DEFAULT_* values
- CORS_ORIGINS to your domain(s)

## 2. Build & start
```bash
cd deploy/docker
# Build and start containers
docker compose -f docker-compose.prod.yml up -d --build
```

## 3. Check status
```bash
docker compose -f docker-compose.prod.yml ps
docker compose -f docker-compose.prod.yml logs -f backend
```

## 4. Access
- Frontend: http://SERVER_IP/
- API docs (through direct backend port if you temporarily map it) else via proxy `/api/*`.
- Health: http://SERVER_IP/healthz

## 5. Volumes (Persistence)
- PostgreSQL data: `pg_data`
- Uploaded files: `backend_uploads`

Backup example:
```bash
# DB backup
PG=$(docker compose -f docker-compose.prod.yml ps -q db)
docker exec -t $PG pg_dump -U ${POSTGRES_USER} ${POSTGRES_DB} > backup_$(date +%Y%m%d_%H%M%S).sql
```

## 6. Common operations
```bash
# Rebuild after code changes
docker compose -f docker-compose.prod.yml up -d --build
# Stop
docker compose -f docker-compose.prod.yml down
# Stop and remove volumes (DANGEROUS)
docker compose -f docker-compose.prod.yml down -v
# Restart only backend
docker compose -f docker-compose.prod.yml restart backend
```

## 7. Database
1. Set `DATABASE_URL` in `.env.postgres`.
2. Run: `docker compose -f docker-compose.prod.yml up -d postgresql`.
3. Migrations are applied automatically on backend startup.
4. Use standard `pg_dump`/`psql` for backups and restore.

## 8. Security
- Use strong `SECRET_KEY`.
- Restrict `CORS_ORIGINS`.
- Use HTTPS via reverse proxy (Caddy/Traefik/Nginx) in front of this stack.

## 9. Health & Troubleshooting
```bash
curl -v http://SERVER_IP/healthz
curl -v http://SERVER_IP/api/materials
```
Check container logs for backend/db errors.

---
Ready for production baseline. Adjust gunicorn workers via `APP_WORKERS` in env as needed.
