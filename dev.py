#!/usr/bin/env python3
"""
简单的开发环境启动脚本
替代复杂的local_dev方式
"""
import subprocess
import sys
import time
import platform
from pathlib import Path

def run_command(cmd, shell=True, check=False):
    """运行命令"""
    try:
        return subprocess.run(cmd, shell=shell, check=check, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
        return e

def start_backend():
    """启动后端服务"""
    print("🚀 启动后端服务...")
    backend_dir = Path("backend")
    
    if platform.system() == "Windows":
        cmd = "start cmd /k \"python run_server.py\""
        subprocess.Popen(cmd, shell=True, cwd=backend_dir)
    else:
        cmd = "python run_server.py"
        subprocess.Popen(cmd, shell=True, cwd=backend_dir)

def start_frontend():
    """启动前端服务"""
    print("🌐 启动前端服务...")
    frontend_dir = Path("frontend")
    
    if platform.system() == "Windows":
        cmd = "start cmd /k \"npm run dev\""
        subprocess.Popen(cmd, shell=True, cwd=frontend_dir)
    else:
        cmd = "npm run dev"
        subprocess.Popen(cmd, shell=True, cwd=frontend_dir)

def main():
    """主函数"""
    print("=" * 50)
    print("🎯 CS素材库 - 开发环境启动")
    print("=" * 50)
    
    # 启动后端
    start_backend()
    
    # 等待一会儿
    print("⏳ 等待后端服务启动...")
    time.sleep(3)
    
    # 启动前端
    start_frontend()
    
    print("\n" + "=" * 50)
    print("✅ 服务启动完成！")
    print("🔗 前端服务: http://localhost:3000")
    print("🔗 后端服务: http://127.0.0.1:8000")
    print("📖 API文档: http://127.0.0.1:8000/docs")
    print("=" * 50)
    
    if platform.system() != "Windows":
        print("\n按 Ctrl+C 退出")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 服务已停止")

if __name__ == "__main__":
    main()
