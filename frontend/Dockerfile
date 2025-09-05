# Frontend Development Dockerfile
# Optimized for development with hot reload

FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files for dependency installation
# This layer will only be rebuilt when package.json or package-lock.json changes
COPY package*.json ./

# Install dependencies
# Use npm ci for faster, reliable builds in CI/CD environments
RUN npm ci

# Copy application source code
# In development, this will be overridden by volume mount
COPY . .

# Expose Vite development server port
EXPOSE 3000

# Health check for development
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/ || exit 1

# Start development server with hot reload
# --host 0.0.0.0 allows external connections (required for Docker)
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
