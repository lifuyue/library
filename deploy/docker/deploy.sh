#!/bin/bash

# CS素材库部署脚本 - Docker 版本

set -e

echo "🚀 开始部署 CS素材库..."

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose 未安装，请先安装 Docker Compose"
    exit 1
fi

# 检查环境变量文件
if [ ! -f .env ]; then
    echo "📝 创建环境变量文件..."
    cat > .env << EOF
SECRET_KEY=$(openssl rand -hex 32)
DATABASE_URL=sqlite:///./cs_library.db
CORS_ORIGINS=http://localhost:3000,http://localhost:80
ENVIRONMENT=production
EOF
    echo "✅ 环境变量文件已创建，请根据需要修改 .env 文件"
fi

# 停止现有容器
echo "🛑 停止现有容器..."
docker-compose down || true

# 构建和启动服务
echo "🔧 构建镜像..."
docker-compose build --no-cache

echo "🚀 启动服务..."
docker-compose up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 健康检查
echo "🔍 检查服务状态..."
if curl -f http://localhost/api/health &> /dev/null; then
    echo "✅ 后端服务正常"
else
    echo "❌ 后端服务异常"
    docker-compose logs backend
    exit 1
fi

if curl -f http://localhost/ &> /dev/null; then
    echo "✅ 前端服务正常"
else
    echo "❌ 前端服务异常"
    docker-compose logs frontend
    exit 1
fi

echo "🎉 部署完成！"
echo "📱 前端地址: http://localhost"
echo "🔧 后端地址: http://localhost:8000"
echo "📊 查看日志: docker-compose logs -f"
