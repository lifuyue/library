@echo off
REM CS素材库部署脚本 - Windows 版本

echo 🚀 开始部署 CS素材库...

REM 检查 Docker 是否安装
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker 未安装，请先安装 Docker Desktop
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose 未安装，请先安装 Docker Compose
    pause
    exit /b 1
)

REM 检查环境变量文件
if not exist .env (
    echo 📝 创建环境变量文件...
    (
        echo SECRET_KEY=your-secret-key-here-change-this
        echo DATABASE_URL=sqlite:///./cs_library.db
        echo CORS_ORIGINS=http://localhost:3000,http://localhost:80
        echo ENVIRONMENT=production
    ) > .env
    echo ✅ 环境变量文件已创建，请根据需要修改 .env 文件
)

REM 停止现有容器
echo 🛑 停止现有容器...
docker-compose down

REM 构建和启动服务
echo 🔧 构建镜像...
docker-compose build --no-cache

echo 🚀 启动服务...
docker-compose up -d

REM 等待服务启动
echo ⏳ 等待服务启动...
timeout /t 10 /nobreak >nul

echo 🎉 部署完成！
echo 📱 前端地址: http://localhost
echo 🔧 后端地址: http://localhost:8000
echo 📊 查看日志: docker-compose logs -f

pause
