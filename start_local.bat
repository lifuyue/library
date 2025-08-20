@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

:: CS素材库本地开发环境启动脚本
:: 支持自动检测端口占用、进程管理、智能启动

echo ================================================
echo 🎯 CS素材库本地开发环境启动器
echo ================================================
echo.

:: 配置变量
set "PROJECT_ROOT=%~dp0"
set "BACKEND_DIR=%PROJECT_ROOT%backend"
set "FRONTEND_DIR=%PROJECT_ROOT%frontend"
set "VENV_DIR=%PROJECT_ROOT%.venv"
set "PYTHON_EXE=%VENV_DIR%\Scripts\python.exe"
set "UVICORN_EXE=%VENV_DIR%\Scripts\uvicorn.exe"
set "BACKEND_PORT=8000"
set "FRONTEND_PORT=3000"

:: 解析命令行参数
set "MODE=full"
set "CLEAN_ONLY=false"
set "FORCE_KILL=false"

:parse_args
if "%~1"=="" goto :args_done
if /i "%~1"=="--backend-only" set "MODE=backend" & shift & goto :parse_args
if /i "%~1"=="--frontend-only" set "MODE=frontend" & shift & goto :parse_args
if /i "%~1"=="--clean" set "CLEAN_ONLY=true" & shift & goto :parse_args
if /i "%~1"=="--force" set "FORCE_KILL=true" & shift & goto :parse_args
if /i "%~1"=="--help" goto :show_help
shift
goto :parse_args

:args_done

:: 如果只是清理，执行清理后退出
if "%CLEAN_ONLY%"=="true" (
    echo 🧹 清理端口占用...
    call :kill_port %BACKEND_PORT%
    call :kill_port %FRONTEND_PORT%
    echo ✅ 清理完成
    goto :end
)

:: 检查依赖
echo 🔍 检查项目依赖...
call :check_dependencies
if !errorlevel! neq 0 goto :error

:: 清理可能存在的端口占用
echo 🧹 清理端口占用...
call :kill_port %BACKEND_PORT%
call :kill_port %FRONTEND_PORT%

:: 启动服务
if "%MODE%"=="full" (
    call :start_backend
    if !errorlevel! neq 0 goto :error
    call :start_frontend
    if !errorlevel! neq 0 goto :error
) else if "%MODE%"=="backend" (
    call :start_backend
    if !errorlevel! neq 0 goto :error
) else if "%MODE%"=="frontend" (
    call :start_frontend
    if !errorlevel! neq 0 goto :error
)

:: 显示成功信息
echo.
echo ================================================
echo 🎉 服务启动成功！
echo ================================================
if "%MODE%"=="full" (
    echo 🔧 后端服务: http://127.0.0.1:%BACKEND_PORT%
    echo 📚 API文档: http://127.0.0.1:%BACKEND_PORT%/docs
    echo 🌐 前端服务: http://localhost:%FRONTEND_PORT%
) else if "%MODE%"=="backend" (
    echo 🔧 后端服务: http://127.0.0.1:%BACKEND_PORT%
    echo 📚 API文档: http://127.0.0.1:%BACKEND_PORT%/docs
) else if "%MODE%"=="frontend" (
    echo 🌐 前端服务: http://localhost:%FRONTEND_PORT%
)
echo.
echo 💡 按任意键停止所有服务...
echo ================================================

pause > nul

:: 停止服务
echo.
echo 🛑 停止所有服务...
call :kill_port %BACKEND_PORT%
call :kill_port %FRONTEND_PORT%
echo ✅ 所有服务已停止
goto :end

:: =============================================================================
:: 函数定义
:: =============================================================================

:check_dependencies
echo   检查虚拟环境...
if not exist "%VENV_DIR%" (
    echo ❌ 未找到虚拟环境，请先创建虚拟环境并安装依赖
    exit /b 1
)

if not exist "%PYTHON_EXE%" (
    echo ❌ 未找到Python可执行文件: %PYTHON_EXE%
    exit /b 1
)

echo   检查后端文件...
if not exist "%BACKEND_DIR%\main.py" (
    echo ❌ 未找到后端main.py文件
    exit /b 1
)

echo   检查前端文件...
if not exist "%FRONTEND_DIR%\package.json" (
    echo ❌ 未找到前端package.json文件
    exit /b 1
)

if not exist "%FRONTEND_DIR%\node_modules" (
    echo   ⚠️  前端依赖未安装，正在安装...
    cd /d "%FRONTEND_DIR%"
    call npm install
    if !errorlevel! neq 0 (
        echo ❌ 前端依赖安装失败
        exit /b 1
    )
    cd /d "%PROJECT_ROOT%"
)

echo ✅ 依赖检查通过
exit /b 0

:check_port
:: 检查端口是否被占用
set "port=%~1"
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":%port% "') do (
    if "%%a" neq "" (
        exit /b 1
    )
)
exit /b 0

:get_port_pid
:: 获取占用端口的进程ID
set "port=%~1"
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":%port% " ^| findstr "LISTENING"') do (
    set "pid=%%a"
    exit /b 0
)
set "pid="
exit /b 1

:kill_port
:: 杀死占用指定端口的进程
set "port=%~1"
call :check_port %port%
if !errorlevel! equ 0 exit /b 0

echo   发现端口 %port% 被占用，正在关闭...
call :get_port_pid %port%
if "!pid!" neq "" (
    taskkill /F /PID !pid! > nul 2>&1
    if !errorlevel! equ 0 (
        echo   ✅ 已关闭占用端口 %port% 的进程 (PID: !pid!)
        timeout /t 2 /nobreak > nul
    ) else (
        echo   ⚠️  无法关闭进程 !pid!
    )
) else (
    echo   ⚠️  无法找到占用端口 %port% 的进程
)
exit /b 0

:start_backend
echo 🚀 启动后端服务...

:: 检查端口是否仍被占用
call :check_port %BACKEND_PORT%
if !errorlevel! neq 0 (
    echo   ⚠️  端口 %BACKEND_PORT% 仍被占用，尝试使用其他端口...
    set /a "BACKEND_PORT+=1"
    call :check_port !BACKEND_PORT!
    if !errorlevel! neq 0 (
        echo ❌ 无法找到可用端口启动后端服务
        exit /b 1
    )
    echo   使用端口: !BACKEND_PORT!
)

:: 启动后端服务
cd /d "%BACKEND_DIR%"
start "CS-Backend" cmd /k ""%UVICORN_EXE%" main:app --host 127.0.0.1 --port %BACKEND_PORT% --reload"

:: 等待服务启动
echo   ⏳ 等待后端服务启动 (端口: %BACKEND_PORT%)...
set "attempts=0"
:wait_backend
set /a "attempts+=1"
if !attempts! gtr 30 (
    echo ❌ 后端服务启动超时
    exit /b 1
)

call :check_port %BACKEND_PORT%
if !errorlevel! equ 0 (
    timeout /t 1 /nobreak > nul
    goto :wait_backend
)

echo ✅ 后端服务启动成功: http://127.0.0.1:%BACKEND_PORT%
cd /d "%PROJECT_ROOT%"
exit /b 0

:start_frontend
echo 🚀 启动前端服务...

:: 检查端口是否仍被占用
call :check_port %FRONTEND_PORT%
if !errorlevel! neq 0 (
    echo   ⚠️  端口 %FRONTEND_PORT% 仍被占用，尝试使用其他端口...
    set /a "FRONTEND_PORT+=1"
    call :check_port !FRONTEND_PORT!
    if !errorlevel! neq 0 (
        echo ❌ 无法找到可用端口启动前端服务
        exit /b 1
    )
    echo   使用端口: !FRONTEND_PORT!
)

:: 启动前端服务
cd /d "%FRONTEND_DIR%"
set "PORT=%FRONTEND_PORT%"
start "CS-Frontend" cmd /k "npm run dev"

:: 等待服务启动
echo   ⏳ 等待前端服务启动 (端口: %FRONTEND_PORT%)...
set "attempts=0"
:wait_frontend
set /a "attempts+=1"
if !attempts! gtr 60 (
    echo ❌ 前端服务启动超时
    exit /b 1
)

call :check_port %FRONTEND_PORT%
if !errorlevel! equ 0 (
    timeout /t 1 /nobreak > nul
    goto :wait_frontend
)

echo ✅ 前端服务启动成功: http://localhost:%FRONTEND_PORT%
cd /d "%PROJECT_ROOT%"
exit /b 0

:show_help
echo 用法: %~nx0 [选项]
echo.
echo 选项:
echo   --backend-only    仅启动后端服务
echo   --frontend-only   仅启动前端服务
echo   --clean          仅清理端口占用，不启动服务
echo   --force          强制关闭占用端口的进程
echo   --help           显示此帮助信息
echo.
echo 示例:
echo   %~nx0                    启动全部服务
echo   %~nx0 --backend-only     仅启动后端
echo   %~nx0 --clean           清理端口占用
goto :end

:error
echo.
echo ❌ 启动失败，请检查错误信息
pause
exit /b 1

:end
endlocal
