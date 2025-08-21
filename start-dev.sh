#!/bin/bash

echo "==========================================="
echo "CS素材库 - 开发环境启动"
echo "==========================================="

echo ""
echo "启动后端服务..."
cd backend && python run_server.py &
BACKEND_PID=$!

echo ""
echo "等待后端服务启动..."
sleep 3

echo ""
echo "启动前端服务..."
cd ../frontend && npm run dev &
FRONTEND_PID=$!

echo ""
echo "==========================================="
echo "服务启动完成！"
echo "后端服务: http://127.0.0.1:8000"
echo "前端服务: http://localhost:3000"
echo "API文档: http://127.0.0.1:8000/docs"
echo "==========================================="
echo ""
echo "按 Ctrl+C 停止所有服务"

# 等待用户中断
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
