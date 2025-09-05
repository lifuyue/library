#!/bin/bash
set -e

echo "🚀 CS素材库 PostgreSQL 部署脚本"
echo "================================"

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    echo "macOS: brew install docker"
    echo "Ubuntu: sudo apt-get install docker.io docker-compose-plugin"
    exit 1
fi

# 检查 Docker Compose 是否可用 (优先使用新版 docker compose)
if docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
elif command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
else
    echo "❌ Docker Compose 未安装或版本过低"
    echo "请安装支持 'docker compose' 命令的版本"
    exit 1
fi

echo "🔧 使用命令: $COMPOSE_CMD"

# 检查环境配置文件
if [ ! -f ".env.deploy" ]; then
    echo "❌ 环境配置文件 .env.deploy 不存在"
    exit 1
fi

echo "⚙️  使用环境配置: .env.deploy"
echo ""
echo "⚠️  生产环境请务必修改以下配置："
echo "   - POSTGRES_PASSWORD"
echo "   - SECRET_KEY" 
echo "   - ADMIN_DEFAULT_PASSWORD"
echo ""

# 询问是否继续
read -p "是否继续部署？(y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 部署取消"
    exit 1
fi

echo "🏗️  开始构建和启动服务..."
echo ""

# 停止可能存在的旧服务
echo "🛑 停止旧服务..."
$COMPOSE_CMD down 2>/dev/null || true

# 构建并启动服务
echo "� 构建镜像..."
$COMPOSE_CMD build --no-cache

echo "🚀 启动服务..."
$COMPOSE_CMD up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo ""
echo "� 服务状态："
$COMPOSE_CMD ps

# 等待数据库健康检查
echo ""
echo "🔍 等待数据库就绪..."
for i in {1..30}; do
    if $COMPOSE_CMD exec -T postgresql pg_isready -U ${POSTGRES_USER:-csuser} >/dev/null 2>&1; then
        echo "✅ 数据库就绪"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ 数据库启动超时"
        $COMPOSE_CMD logs postgresql
        exit 1
    fi
    sleep 2
done

# 等待后端服务
echo ""
echo "🔍 等待后端服务..."
for i in {1..60}; do
    if curl -f http://localhost:8000/api/health >/dev/null 2>&1; then
        echo "✅ 后端服务就绪"
        break
    fi
    if [ $i -eq 60 ]; then
        echo "❌ 后端服务启动超时"
        $COMPOSE_CMD logs cslibrary-backend
        exit 1
    fi
    sleep 2
done

echo ""
echo "🎉 部署成功！"
echo ""
echo "� 服务地址："
echo "   后端 API: http://localhost:8000"
echo "   API 文档: http://localhost:8000/docs"
echo "   前端页面: http://localhost:80"
echo ""
echo "� 默认管理员账号："
echo "   用户名: admin"
echo "   密码: admin123"
echo "   (请尽快修改密码)"
echo ""
echo "🔧 管理命令："
echo "   查看日志: $COMPOSE_CMD logs -f"
echo "   停止服务: $COMPOSE_CMD down"
echo "   重启服务: $COMPOSE_CMD restart"
echo ""
echo "💾 数据备份："
echo "   备份数据库: $COMPOSE_CMD exec postgresql pg_dump -U ${POSTGRES_USER:-csuser} ${POSTGRES_DB:-cslibrary} > backup_\$(date +%Y%m%d_%H%M%S).sql"
echo ""
