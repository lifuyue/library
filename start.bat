@echo off
echo 正在启动CS素材库项目...
echo.

echo 1. 激活虚拟环境...
call .venv\Scripts\activate.bat

echo 2. 启动后端服务...
start cmd /k "cd backend && python main.py"

echo 3. 等待后端启动...
timeout /t 3 /nobreak >nul

echo 4. 安装前端依赖（如果需要）...
cd frontend
if not exist node_modules (
    echo 正在安装前端依赖...
    npm install
)

echo 5. 启动前端开发服务器...
start cmd /k "npm run dev"

echo.
echo 项目启动完成！
echo 前端地址: http://localhost:3000
echo 后端地址: http://localhost:8000
echo API文档: http://localhost:8000/docs
echo.
pause
