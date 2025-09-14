#!/bin/bash

echo "正在启动CS素材库项目..."
echo

echo "1. 激活虚拟环境..."
source .venv/bin/activate

echo "2. 启动后端服务..."
cd backend
python main.py &
BACKEND_PID=$!

echo "3. 等待后端启动..."
sleep 3

echo "4. 安装前端依赖（如果需要）..."
cd ../web
if [ ! -d "node_modules" ]; then
    echo "正在安装前端依赖..."
    npm install
fi

echo "5. 启动前端开发服务器..."
npm run dev &
FRONTEND_PID=$!

echo
echo "项目启动完成！"
echo "前端地址: http://localhost:3000"
echo "后端地址: http://localhost:8000"
echo "API文档: http://localhost:8000/docs"
echo
echo "按 Ctrl+C 停止所有服务"

# 等待用户中断
wait
