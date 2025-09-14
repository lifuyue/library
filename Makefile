# Project Makefile — convenience commands for dev and prod

SHELL := /bin/bash
.SHELLFLAGS := -euo pipefail -c
.ONESHELL:
COMPOSE_STACK := deploy/docker/docker-compose.yml

COMPOSE_DEV := docker-compose.dev.yml
COMPOSE_PROD := docker-compose.prod.yml

.PHONY: help
help:
	@echo "Common commands:"
	@echo "  make dev            # Start dev (foreground)"
	@echo "  make dev-up         # Start dev (foreground)"
	@echo "  make dev-up-d       # Start dev (detached)"
	@echo "  make dev-build      # Rebuild and start dev"
	@echo "  make dev-down       # Stop dev"
	@echo "  make dev-logs       # Tail dev logs"
	@echo "  make sh-backend     # Shell into dev backend"
	@echo "  make sh-frontend    # Shell into dev frontend"
	@echo "  make prod-up        # Start prod (detached)"
	@echo "  make prod-build     # Rebuild and start prod"
	@echo "  make prod-down      # Stop prod"
	@echo "  make prod-logs      # Tail prod logs"
	@echo "  make check-backend  # Quick Python syntax check"
	@echo "  make build-frontend # Local frontend build"
	@echo "  make docker-build   # Build backend+frontend images"
	@echo "  make docker-up      # Up stack (detached)"
	@echo "  make docker-down    # Down stack"
	@echo "  make docker-logs    # Tail stack logs"
	@echo "  make clean          # Remove containers, networks, volumes"

# ----- Development -----
.PHONY: dev dev-up dev-up-d dev-build dev-down dev-logs sh-backend sh-frontend

dev: dev-up

dev-up:
	docker compose -f $(COMPOSE_DEV) up

dev-up-d:
	docker compose -f $(COMPOSE_DEV) up -d

dev-build:
	docker compose -f $(COMPOSE_DEV) up --build

dev-down:
	docker compose -f $(COMPOSE_DEV) down

dev-logs:
	docker compose -f $(COMPOSE_DEV) logs -f --tail=200

sh-backend:
	docker compose -f $(COMPOSE_DEV) exec backend bash || docker compose -f $(COMPOSE_DEV) exec backend sh

sh-frontend:
	docker compose -f $(COMPOSE_DEV) exec frontend sh

# ----- Database Utilities -----
.PHONY: db-up db-migrate db-upgrade

db-up:
	docker compose -f $(COMPOSE_DEV) up -d db

db-migrate:
	docker compose -f $(COMPOSE_DEV) exec backend alembic revision --autogenerate -m "$(m)"

db-upgrade:
	docker compose -f $(COMPOSE_DEV) exec backend alembic upgrade head

# ----- Production -----
.PHONY: prod-up prod-build prod-down prod-logs

prod-up:
	docker compose -f $(COMPOSE_PROD) up -d

prod-build:
	docker compose -f $(COMPOSE_PROD) up --build -d

prod-down:
	docker compose -f $(COMPOSE_PROD) down

prod-logs:
	docker compose -f $(COMPOSE_PROD) logs -f --tail=200

# ----- Local checks (non-Docker) -----
.PHONY: check-backend build-frontend

check-backend:
	@echo "Python syntax check (backend)"
	@python3 -c "import os,sys,py_compile;files=[os.path.join(d,f) for r in ['backend'] for d,_,fs in os.walk(r) for f in fs if f.endswith('.py')];[py_compile.compile(f,doraise=True) for f in files];print('All Python files OK')"

build-frontend:
	cd frontend && npm ci && npm run build

# ----- Utilities -----
.PHONY: clean
clean:
	@echo "Removing dev containers, networks, and volumes..."
	docker compose -f $(COMPOSE_DEV) down -v || true
	@echo "Removing prod containers, networks, and volumes..."
	docker compose -f $(COMPOSE_PROD) down -v || true

.PHONY: docker-build docker-up docker-down docker-logs
docker-build:
	docker compose -f $(COMPOSE_STACK) build
docker-up:
	docker compose -f $(COMPOSE_STACK) up -d
docker-down:
	docker compose -f $(COMPOSE_STACK) down
docker-logs:
	docker compose -f $(COMPOSE_STACK) logs -f --tail=200
