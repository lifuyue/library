#!/bin/bash

# CS素材库本地开发环境启动脚本
# 支持自动检测端口占用、进程管理、智能启动

set -e

# 配置变量
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"
FRONTEND_DIR="$PROJECT_ROOT/frontend"
VENV_DIR="$PROJECT_ROOT/.venv"
PYTHON_EXE="$VENV_DIR/bin/python"
UVICORN_EXE="$VENV_DIR/bin/uvicorn"
BACKEND_PORT=8000
FRONTEND_PORT=3000

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 默认参数
MODE="full"
CLEAN_ONLY=false

# 帮助信息
show_help() {
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  --backend-only    仅启动后端服务"
    echo "  --frontend-only   仅启动前端服务"
    echo "  --clean          仅清理端口占用，不启动服务"
    echo "  --help           显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0                    启动全部服务"
    echo "  $0 --backend-only     仅启动后端"
    echo "  $0 --clean           清理端口占用"
}

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --backend-only)
            MODE="backend"
            shift
            ;;
        --frontend-only)
            MODE="frontend"
            shift
            ;;
        --clean)
            CLEAN_ONLY=true
            shift
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            echo "未知选项: $1"
            show_help
            exit 1
            ;;
    esac
done

# 检查端口是否被占用
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0  # 端口被占用
    else
        return 1  # 端口可用
    fi
}

# 获取占用端口的进程ID
get_port_pid() {
    local port=$1
    lsof -ti:$port 2>/dev/null
}

# 杀死占用指定端口的进程
kill_port() {
    local port=$1
    if check_port $port; then
        echo -e "${BLUE}🔄 发现端口 $port 被占用，正在关闭...${NC}"
        local pid=$(get_port_pid $port)
        if [[ -n "$pid" ]]; then
            kill -9 $pid 2>/dev/null
            if [[ $? -eq 0 ]]; then
                echo -e "${GREEN}✅ 已关闭占用端口 $port 的进程 (PID: $pid)${NC}"
                sleep 1  # 等待端口释放
            else
                echo -e "${YELLOW}⚠️  无法关闭进程 $pid${NC}"
            fi
        else
            echo -e "${YELLOW}⚠️  无法找到占用端口 $port 的进程${NC}"
        fi
    fi
}

# 检查依赖
check_dependencies() {
    echo -e "${BLUE}🔍 检查项目依赖...${NC}"
    
    if [[ ! -d "$VENV_DIR" ]]; then
        echo -e "${RED}❌ 未找到虚拟环境，请先创建虚拟环境并安装依赖${NC}"
        exit 1
    fi

    if [[ ! -f "$PYTHON_EXE" ]]; then
        echo -e "${RED}❌ 未找到Python可执行文件: $PYTHON_EXE${NC}"
        exit 1
    fi

    if [[ ! -f "$BACKEND_DIR/main.py" ]]; then
        echo -e "${RED}❌ 未找到后端main.py文件${NC}"
        exit 1
    fi

    if [[ ! -f "$FRONTEND_DIR/package.json" ]]; then
        echo -e "${RED}❌ 未找到前端package.json文件${NC}"
        exit 1
    fi

    if [[ ! -d "$FRONTEND_DIR/node_modules" ]]; then
        echo -e "${YELLOW}⚠️  前端依赖未安装，正在安装...${NC}"
        cd "$FRONTEND_DIR"
        npm install
        if [[ $? -ne 0 ]]; then
            echo -e "${RED}❌ 前端依赖安装失败${NC}"
            exit 1
        fi
        cd "$PROJECT_ROOT"
    fi

    echo -e "${GREEN}✅ 依赖检查通过${NC}"
}

# 启动后端服务
start_backend() {
    echo -e "${BLUE}🚀 启动后端服务...${NC}"
    
    # 检查端口是否仍被占用
    if check_port $BACKEND_PORT; then
        echo -e "${YELLOW}⚠️  端口 $BACKEND_PORT 仍被占用，尝试使用其他端口...${NC}"
        ((BACKEND_PORT++))
        if check_port $BACKEND_PORT; then
            echo -e "${RED}❌ 无法找到可用端口启动后端服务${NC}"
            exit 1
        fi
        echo -e "${BLUE}使用端口: $BACKEND_PORT${NC}"
    fi

    # 启动后端服务
    cd "$BACKEND_DIR"
    "$UVICORN_EXE" main:app --host 127.0.0.1 --port $BACKEND_PORT --reload &
    BACKEND_PID=$!

    # 等待服务启动
    echo -e "${BLUE}⏳ 等待后端服务启动 (端口: $BACKEND_PORT)...${NC}"
    for i in {1..30}; do
        if check_port $BACKEND_PORT; then
            echo -e "${GREEN}✅ 后端服务启动成功: http://127.0.0.1:$BACKEND_PORT${NC}"
            echo -e "${GREEN}📖 API文档地址: http://127.0.0.1:$BACKEND_PORT/docs${NC}"
            cd "$PROJECT_ROOT"
            return 0
        fi
        sleep 1
    done

    echo -e "${RED}❌ 后端服务启动超时${NC}"
    cd "$PROJECT_ROOT"
    exit 1
}

# 启动前端服务
start_frontend() {
    echo -e "${BLUE}🚀 启动前端服务...${NC}"
    
    # 检查端口是否仍被占用
    if check_port $FRONTEND_PORT; then
        echo -e "${YELLOW}⚠️  端口 $FRONTEND_PORT 仍被占用，尝试使用其他端口...${NC}"
        ((FRONTEND_PORT++))
        if check_port $FRONTEND_PORT; then
            echo -e "${RED}❌ 无法找到可用端口启动前端服务${NC}"
            exit 1
        fi
        echo -e "${BLUE}使用端口: $FRONTEND_PORT${NC}"
    fi

    # 启动前端服务
    cd "$FRONTEND_DIR"
    PORT=$FRONTEND_PORT npm run dev &
    FRONTEND_PID=$!

    # 等待服务启动
    echo -e "${BLUE}⏳ 等待前端服务启动 (端口: $FRONTEND_PORT)...${NC}"
    for i in {1..60}; do
        if check_port $FRONTEND_PORT; then
            echo -e "${GREEN}✅ 前端服务启动成功: http://localhost:$FRONTEND_PORT${NC}"
            cd "$PROJECT_ROOT"
            return 0
        fi
        sleep 1
    done

    echo -e "${RED}❌ 前端服务启动超时${NC}"
    cd "$PROJECT_ROOT"
    exit 1
}

# 清理函数
cleanup() {
    echo ""
    echo -e "${BLUE}🛑 停止所有服务...${NC}"
    kill_port $BACKEND_PORT
    kill_port $FRONTEND_PORT
    
    # 杀死可能的后台进程
    if [[ -n "$BACKEND_PID" ]]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    if [[ -n "$FRONTEND_PID" ]]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    
    echo -e "${GREEN}✅ 所有服务已停止${NC}"
    exit 0
}

# 设置信号处理
trap cleanup SIGINT SIGTERM

# 主函数
main() {
    echo "================================================"
    echo -e "${BLUE}🎯 CS素材库本地开发环境启动器${NC}"
    echo "================================================"
    echo ""

    # 如果只是清理，执行清理后退出
    if [[ "$CLEAN_ONLY" == "true" ]]; then
        echo -e "${BLUE}🧹 清理端口占用...${NC}"
        kill_port $BACKEND_PORT
        kill_port $FRONTEND_PORT
        echo -e "${GREEN}✅ 清理完成${NC}"
        exit 0
    fi

    # 检查依赖
    check_dependencies

    # 清理可能存在的端口占用
    echo -e "${BLUE}🧹 清理端口占用...${NC}"
    kill_port $BACKEND_PORT
    kill_port $FRONTEND_PORT

    # 启动服务
    case $MODE in
        "full")
            start_backend
            start_frontend
            ;;
        "backend")
            start_backend
            ;;
        "frontend")
            start_frontend
            ;;
    esac

    # 显示成功信息
    echo ""
    echo "================================================"
    echo -e "${GREEN}🎉 服务启动成功！${NC}"
    echo "================================================"
    
    case $MODE in
        "full")
            echo -e "${GREEN}🔧 后端服务: http://127.0.0.1:$BACKEND_PORT${NC}"
            echo -e "${GREEN}📚 API文档: http://127.0.0.1:$BACKEND_PORT/docs${NC}"
            echo -e "${GREEN}🌐 前端服务: http://localhost:$FRONTEND_PORT${NC}"
            ;;
        "backend")
            echo -e "${GREEN}🔧 后端服务: http://127.0.0.1:$BACKEND_PORT${NC}"
            echo -e "${GREEN}📚 API文档: http://127.0.0.1:$BACKEND_PORT/docs${NC}"
            ;;
        "frontend")
            echo -e "${GREEN}🌐 前端服务: http://localhost:$FRONTEND_PORT${NC}"
            ;;
    esac
    
    echo ""
    echo -e "${BLUE}💡 按 Ctrl+C 停止所有服务...${NC}"
    echo "================================================"

    # 保持运行
    while true; do
        sleep 1
    done
}

# 运行主函数
main
