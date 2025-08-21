#!/usr/bin/env python3
"""
CS素材库后端服务启动脚本
简单的启动入口，可以直接运行启动后端服务
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """启动后端服务"""
    # 获取项目根目录和后端目录
    current_dir = Path(__file__).parent
    project_root = current_dir.parent
    backend_dir = current_dir
    
    # 优先选择 backend 目录下的 .venv，然后再尝试项目根目录的 .venv
    candidates = [backend_dir / ".venv", project_root / ".venv"]
    venv_dir = None
    for cand in candidates:
        if cand.exists():
            venv_dir = cand
            break
    if venv_dir is None:
        # 若都不存在，保持原先行为（会在后面报错并提示创建虚拟环境）
        venv_dir = project_root / ".venv"

    if os.name == 'nt':  # Windows
        python_exe = venv_dir / "Scripts" / "python.exe"
        uvicorn_exe = venv_dir / "Scripts" / "uvicorn.exe"
    else:  # Linux/Mac
        python_exe = venv_dir / "bin" / "python"
        uvicorn_exe = venv_dir / "bin" / "uvicorn"
    
    # 检查 python 可执行文件是否存在
    if not python_exe.exists():
        print("❌ 虚拟环境未找到，请先创建虚拟环境")
        print(f"期望路径: {python_exe}")
        sys.exit(1)
    
    # 检查 uvicorn：优先看可执行文件，其次尝试用 `python -m uvicorn` 导入模块检查
    use_python_module = False
    if uvicorn_exe.exists():
        uvicorn_available = True
    else:
        # 尝试导入 uvicorn 模块，若成功则使用 `python -m uvicorn` 启动
        try:
            subprocess.run([str(python_exe), "-c", "import importlib; importlib.import_module('uvicorn')"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            uvicorn_available = True
            use_python_module = True
        except Exception:
            uvicorn_available = False

    if not uvicorn_available:
        print("❌ uvicorn未安装，请运行: pip install uvicorn")
        sys.exit(1)
    
    # 检查main.py是否存在
    main_py = backend_dir / "main.py"
    if not main_py.exists():
        print("❌ main.py文件未找到")
        sys.exit(1)
    
    print("🚀 启动CS素材库后端服务...")
    print(f"📁 工作目录: {backend_dir}")
    print(f"🐍 Python: {python_exe}")
    print(f"🦄 Uvicorn: {uvicorn_exe if not use_python_module else '(via python -m uvicorn)'}")
    
    try:
        # 切换到backend目录并启动服务
        os.chdir(backend_dir)
        
        # 构建启动命令
        if use_python_module:
            cmd = [str(python_exe), "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"]
        else:
            cmd = [str(uvicorn_exe), "main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"]
        
        print(f"🎯 服务地址: http://127.0.0.1:8000")
        print(f"📚 API文档: http://127.0.0.1:8000/docs")
        print("💡 按 Ctrl+C 停止服务")
        print("-" * 50)
        
        # 启动服务
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n🛑 服务已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
