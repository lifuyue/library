# Docker Development and Production Setup

This project provides complete Docker configurations for both development and production environments.

## Quick Start

### Development Mode (Recommended for local development)
```bash
# Start development environment with hot reload
docker compose -f docker-compose.dev.yml up

# Or rebuild and start
docker compose -f docker-compose.dev.yml up --build

# Run in background
docker compose -f docker-compose.dev.yml up -d
```

**Development Features:**
- 🔥 Hot reload for both backend and frontend
- 📁 Source code mounted as volumes (changes reflect immediately)
- 🐍 Backend: Python FastAPI with uvicorn --reload
- ⚛️ Frontend: Node.js with Vite dev server
- 🔧 Easy debugging and development

**Access Points:**
- Backend API: http://localhost:8000
- Frontend: http://localhost:3000
- Backend API docs: http://localhost:8000/docs

### Production Mode
```bash
# Start production environment
docker compose -f docker-compose.prod.yml up -d

# Build and start
docker compose -f docker-compose.prod.yml up --build -d
```

**Production Features:**
- 🚀 Optimized multi-stage builds
- 📦 Minimal image sizes
- 🔒 Security hardened (non-root users)
- 🏥 Health checks included
- 🌐 Nginx for static file serving
- ⚡ Gunicorn for Python WSGI

**Access Points:**
- Backend API: http://localhost:8000
- Frontend: http://localhost:3000 (served by Nginx)

## Environment Variables

### Backend (.env files)
- Development: `backend/.env`
- Production: `backend/.env.prod`

Key variables to configure:
```bash
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
CORS_ORIGINS=http://localhost:3000
```

### Frontend
Environment variables are handled through Vite's built-in system:
- `VITE_API_BASE`: Backend API URL

## File Structure
```
├── docker-compose.yml           # Main development compose (current default)
├── docker-compose.dev.yml       # Development environment
├── docker-compose.prod.yml      # Production environment
├── backend/
│   ├── Dockerfile              # Development Dockerfile
│   ├── Dockerfile.dev          # Development Dockerfile (explicit)
│   ├── Dockerfile.prod         # Production Dockerfile
│   ├── .dockerignore           # Build context exclusions
│   ├── .env                    # Development environment variables
│   └── .env.prod               # Production environment variables
└── web/
    ├── Dockerfile              # Development Dockerfile
    ├── Dockerfile.dev          # Development Dockerfile (explicit)
    ├── Dockerfile.prod         # Production Dockerfile
    ├── nginx.conf              # Nginx configuration for production
    └── .dockerignore           # Build context exclusions
```

## Commands Reference

### Development
```bash
# Start development environment
docker compose -f docker-compose.dev.yml up

# Stop development environment
docker compose -f docker-compose.dev.yml down

# View logs
docker compose -f docker-compose.dev.yml logs -f

# Rebuild specific service
docker compose -f docker-compose.dev.yml up --build backend
```

### Production
```bash
# Start production environment
docker compose -f docker-compose.prod.yml up -d

# Stop production environment
docker compose -f docker-compose.prod.yml down

# View logs
docker compose -f docker-compose.prod.yml logs -f

# Scale services (production)
docker compose -f docker-compose.prod.yml up -d --scale backend=3
```

### Utility Commands
```bash
# Remove all containers, networks, and volumes
docker compose -f docker-compose.dev.yml down -v

# Prune unused Docker resources
docker system prune -a

# Monitor resource usage
docker stats

# Execute commands in running containers
docker compose -f docker-compose.dev.yml exec backend bash
docker compose -f docker-compose.dev.yml exec frontend sh
```

## Switching Between Environments

The project is designed to easily switch between development and production:

1. **Development** (default): Use `docker-compose.dev.yml`
2. **Production**: Use `docker-compose.prod.yml`

## Security Notes for Production

1. **Change default passwords** in `.env.prod`
2. **Use secure SECRET_KEY** for JWT tokens
3. **Configure CORS_ORIGINS** to match your domain
4. **Use HTTPS** in production with a reverse proxy
5. **Regular security updates** for base images

## Troubleshooting

### Common Issues

1. **Port conflicts**: Ensure ports 8000 and 3000 are available
2. **Volume permissions**: Check Docker Desktop file sharing settings on macOS/Windows
3. **Environment variables**: Verify `.env` files exist and contain required variables
4. **Network connectivity**: Ensure containers can communicate (check `docker network ls`)

### Debugging
```bash
# Check container status
docker compose ps

# View specific service logs
docker compose logs backend
docker compose logs frontend

# Enter container for debugging
docker compose exec backend bash
docker compose exec frontend sh

# Check container resource usage
docker stats
```

For more detailed logs or debugging, you can use:
```bash
# Verbose logging
docker compose --verbose up

# Follow logs from all services
docker compose logs -f --tail=100
```
