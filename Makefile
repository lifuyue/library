# Project Makefile — convenience commands for dev and prod

SHELL := /bin/bash

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
	@python - <<'PY'
import os, sys
roots = ['backend']
files = []
for root in roots:
	for dp, _, fn in os.walk(root):
		for f in fn:
			if f.endswith('.py'):
				files.append(os.path.join(dp, f))
ok = True
for f in files:
	try:
		compile(open(f, 'rb').read(), f, 'exec')
	except Exception as e:
		ok = False
		print(f"Syntax error in {f}: {e}")
sys.exit(0 if ok else 1)
PY

build-frontend:
	cd frontend && npm run build

# ----- Utilities -----
.PHONY: clean
clean:
	@echo "Removing dev containers, networks, and volumes..."
	docker compose -f $(COMPOSE_DEV) down -v || true
	@echo "Removing prod containers, networks, and volumes..."
	docker compose -f $(COMPOSE_PROD) down -v || true

