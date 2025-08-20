#!/usr/bin/env python3
"""
CS素材库本地开发服务启动脚本
支持自动检测端口占用、进程管理、智能启动
"""

import os
import sys
import time
import signal
import subprocess
import argparse
from pathlib import Path
import json
import platform
import socket
import shutil

class LocalDevServer:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_dir = self.project_root / "backend"
        self.frontend_dir = self.project_root / "frontend"
        self.venv_dir = self.project_root / ".venv"
        
        # 默认端口配置
        self.backend_port = 8000
        self.frontend_port = 3000
        
        # 进程存储
        self.processes = {}
        
        # 平台检测
        self.is_windows = platform.system() == "Windows"
        
        # 设置Python和npm可执行文件路径
        if self.is_windows:
            self.python_exe = self.venv_dir / "Scripts" / "python.exe"
            self.uvicorn_exe = self.venv_dir / "Scripts" / "uvicorn.exe"
        else:
            self.python_exe = self.venv_dir / "bin" / "python"
            self.uvicorn_exe = self.venv_dir / "bin" / "uvicorn"

    def check_dependencies(self):
        """检查项目依赖是否满足"""
        print("🔍 检查项目依赖...")
        
        # 检查虚拟环境
        if not self.venv_dir.exists():
            print("❌ 未找到虚拟环境，请先创建虚拟环境并安装依赖")
            return False
            
        # 检查Python可执行文件
        if not self.python_exe.exists():
            print(f"❌ 未找到Python可执行文件: {self.python_exe}")
            return False
            
        # 检查后端依赖
        if not (self.backend_dir / "main.py").exists():
            print("❌ 未找到后端main.py文件")
            return False
            
        # 检查前端依赖
        if not (self.frontend_dir / "package.json").exists():
            print("❌ 未找到前端package.json文件")
            return False
            
        # 检查前端node_modules
        if not (self.frontend_dir / "node_modules").exists():
            print("⚠️  前端依赖未安装，将自动安装...")
            self.install_frontend_deps()
            
        print("✅ 依赖检查通过")
        return True

    def install_frontend_deps(self):
        """安装前端依赖"""
        print("📦 安装前端依赖...")
        npm_cmd = self._resolve_npm_command()
        if not npm_cmd:
            print("❌ 未找到 npm，请先安装 Node.js (https://nodejs.org) 并确保其加入 PATH 环境变量")
            sys.exit(1)
        try:
            subprocess.run(
                [npm_cmd, "install"],
                cwd=self.frontend_dir,
                check=True,
                capture_output=True,
                text=True
            )
            print("✅ 前端依赖安装完成")
        except subprocess.CalledProcessError as e:
            print("❌ 前端依赖安装失败")
            print("--- stdout ---")
            print(e.stdout)
            print("--- stderr ---")
            print(e.stderr)
            sys.exit(1)

    def check_port(self, port):
        """检查端口是否被占用"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            return result == 0
        except:
            return False

    def get_process_using_port(self, port):
        """获取占用端口的进程ID (仅Windows)"""
        if not self.is_windows:
            return None
            
        try:
            cmd = f'netstat -ano | findstr :{port}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if f':{port}' in line and 'LISTENING' in line:
                    parts = line.split()
                    if len(parts) >= 5:
                        return int(parts[-1])
        except:
            pass
        return None

    def kill_process_on_port(self, port):
        """杀死占用指定端口的进程"""
        if not self.check_port(port):
            return True
            
        print(f"🔄 发现端口 {port} 被占用")
        
        if self.is_windows:
            pid = self.get_process_using_port(port)
            if pid:
                try:
                    subprocess.run(f'taskkill /F /PID {pid}', shell=True, check=True, capture_output=True)
                    print(f"✅ 已关闭占用端口 {port} 的进程 (PID: {pid})")
                    time.sleep(1)  # 等待端口释放
                    return True
                except subprocess.CalledProcessError:
                    print(f"⚠️  无法关闭进程 {pid}")
                    return False
        else:
            # Linux/Mac 使用 lsof
            try:
                result = subprocess.run(f'lsof -ti:{port}', shell=True, capture_output=True, text=True)
                if result.stdout.strip():
                    pid = result.stdout.strip()
                    subprocess.run(f'kill -9 {pid}', shell=True, check=True)
                    print(f"✅ 已关闭占用端口 {port} 的进程 (PID: {pid})")
                    time.sleep(1)  # 等待端口释放
                    return True
            except subprocess.CalledProcessError:
                print(f"⚠️  无法关闭占用端口 {port} 的进程")
                return False
        
        return True

    def find_available_port(self, start_port, max_attempts=10):
        """寻找可用端口"""
        for i in range(max_attempts):
            port = start_port + i
            if not self.check_port(port):
                return port
        return None

    def start_backend(self):
        """启动后端服务"""
        print("🚀 启动后端服务...")
        
        # 检查并处理端口占用
        if not self.kill_process_on_port(self.backend_port):
            # 如果无法关闭占用进程，寻找新端口
            new_port = self.find_available_port(self.backend_port + 1)
            if new_port:
                print(f"⚠️  使用备用端口: {new_port}")
                self.backend_port = new_port
            else:
                print("❌ 无法找到可用端口启动后端服务")
                return False

        try:
            # 启动后端服务
            cmd = [
                str(self.uvicorn_exe),
                "main:app",
                "--host", "127.0.0.1",
                "--port", str(self.backend_port),
                "--reload"
            ]
            
            process = subprocess.Popen(
                cmd,
                cwd=self.backend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            self.processes['backend'] = process
            
            # 等待服务启动
            print(f"⏳ 等待后端服务启动 (端口: {self.backend_port})...")
            for i in range(30):  # 最多等待30秒
                if process.poll() is not None:
                    # 进程已退出，读取错误信息
                    output = process.stdout.read()
                    print(f"❌ 后端服务启动失败:\n{output}")
                    return False
                    
                # 检查端口是否被监听
                if self.check_port(self.backend_port):
                    print(f"✅ 后端服务启动成功: http://127.0.0.1:{self.backend_port}")
                    print(f"📖 API文档地址: http://127.0.0.1:{self.backend_port}/docs")
                    return True
                    
                time.sleep(1)
                
            print("❌ 后端服务启动超时")
            return False
            
        except Exception as e:
            print(f"❌ 启动后端服务时出错: {e}")
            return False

    def start_frontend(self):
        """启动前端服务"""
        print("🚀 启动前端服务...")
        
        # 检查并处理端口占用
        if not self.kill_process_on_port(self.frontend_port):
            # 如果无法关闭占用进程，寻找新端口
            new_port = self.find_available_port(self.frontend_port + 1)
            if new_port:
                print(f"⚠️  使用备用端口: {new_port}")
                self.frontend_port = new_port
            else:
                print("❌ 无法找到可用端口启动前端服务")
                return False

        try:
            npm_cmd = self._resolve_npm_command()
            if not npm_cmd:
                print("❌ 未找到 npm，可尝试：重新打开终端 / 安装 Node.js / 检查 PATH")
                return False
            # 设置环境变量
            env = os.environ.copy()
            env['PORT'] = str(self.frontend_port)
            # 给 Vite 一些颜色输出提示
            env.setdefault('FORCE_COLOR', '1')
            
            # 启动前端服务
            # 强制utf-8编码，避免Windows下gbk报错
            env['PYTHONIOENCODING'] = 'utf-8'
            process = subprocess.Popen(
                [npm_cmd, "run", "dev"],
                cwd=self.frontend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                env=env,
                bufsize=1,
                universal_newlines=True,
                encoding="utf-8"
            )
            self.processes['frontend'] = process
            print(f"⏳ 等待前端服务启动 (端口: {self.frontend_port})...")
            # 实时打印子进程输出，并检测端口
            for i in range(60):  # 最多等待60秒
                if process.poll() is not None:
                    # 进程已退出，读取错误信息
                    output = process.stdout.read()
                    print(f"❌ 前端服务启动失败:\n{output}")
                    return False
                # 实时输出
                line = process.stdout.readline()
                if line:
                    print(line.rstrip())
                # 检查端口是否被监听
                if self.check_port(self.frontend_port):
                    print(f"✅ 前端服务启动成功: http://localhost:{self.frontend_port}")
                    return True
                time.sleep(1)
            print("❌ 前端服务启动超时")
            return False
            
        except Exception as e:
            print(f"❌ 启动前端服务时出错: {e}")
            return False

    def _resolve_npm_command(self):
        """定位 npm / npm.cmd，可返回绝对路径或命令名；失败返回 None"""
        # 优先用 shutil.which（能返回绝对路径）
        candidates = []
        if self.is_windows:
            # Windows 上 npm 通常是 npm.cmd
            candidates.extend(["npm.cmd", "npm"])
        else:
            candidates.append("npm")
        for name in candidates:
            path = shutil.which(name)
            if path:
                return path
        return None

    def stop_services(self):
        """停止所有服务"""
        print("🛑 停止所有服务...")
        
        for name, process in self.processes.items():
            if process and process.poll() is None:
                print(f"⏹️  停止{name}服务...")
                try:
                    if self.is_windows:
                        process.terminate()
                    else:
                        process.send_signal(signal.SIGTERM)
                    
                    try:
                        process.wait(timeout=5)
                        print(f"✅ {name}服务已停止")
                    except subprocess.TimeoutExpired:
                        process.kill()
                        print(f"💀 {name}服务已强制停止")
                        
                except Exception as e:
                    print(f"⚠️  停止{name}服务时出错: {e}")

    def cleanup_ports(self):
        """清理端口占用"""
        ports_to_clean = [self.backend_port, self.frontend_port]
        for port in ports_to_clean:
            self.kill_process_on_port(port)

    def signal_handler(self, signum, frame):
        """信号处理器"""
        print("\n🔄 接收到退出信号，正在停止服务...")
        self.stop_services()
        sys.exit(0)

    def run(self, mode="full"):
        """运行开发服务器"""
        print("=" * 50)
        print("🎯 CS素材库本地开发环境启动器")
        print("=" * 50)
        
        # 注册信号处理器
        if hasattr(signal, 'SIGTERM'):
            signal.signal(signal.SIGTERM, self.signal_handler)
        if hasattr(signal, 'SIGINT'):
            signal.signal(signal.SIGINT, self.signal_handler)
        
        try:
            # 检查依赖
            if not self.check_dependencies():
                return False
            
            # 清理可能存在的端口占用
            print("🧹 清理端口占用...")
            self.cleanup_ports()
            
            success = True
            
            # 根据模式启动服务
            if mode in ["full", "backend"]:
                success &= self.start_backend()
                
            if mode in ["full", "frontend"] and success:
                success &= self.start_frontend()
            
            if success:
                print("\n" + "=" * 50)
                print("🎉 服务启动成功！")
                print("=" * 50)
                
                if mode in ["full", "backend"]:
                    print(f"🔧 后端服务: http://127.0.0.1:{self.backend_port}")
                    print(f"📚 API文档: http://127.0.0.1:{self.backend_port}/docs")
                    
                if mode in ["full", "frontend"]:
                    print(f"🌐 前端服务: http://localhost:{self.frontend_port}")
                
                print("\n💡 按 Ctrl+C 停止所有服务")
                print("=" * 50)
                
                # 保持运行
                try:
                    while True:
                        time.sleep(1)
                        # 检查进程是否还在运行
                        for name, process in self.processes.items():
                            if process and process.poll() is not None:
                                print(f"⚠️  {name}服务意外停止")
                                return False
                except KeyboardInterrupt:
                    self.signal_handler(signal.SIGINT, None)
                    
            else:
                print("❌ 服务启动失败")
                self.stop_services()
                return False
                
        except Exception as e:
            print(f"❌ 运行时出错: {e}")
            self.stop_services()
            return False

def main():
    parser = argparse.ArgumentParser(description="CS素材库本地开发环境启动器")
    parser.add_argument(
        "--mode", 
        choices=["full", "backend", "frontend"], 
        default="full",
        help="启动模式: full(全部), backend(仅后端), frontend(仅前端)"
    )
    parser.add_argument(
        "--backend-port",
        type=int,
        default=8000,
        help="后端服务端口 (默认: 8000)"
    )
    parser.add_argument(
        "--frontend-port",
        type=int,
        default=3000,
        help="前端服务端口 (默认: 3000)"
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="仅清理端口占用，不启动服务"
    )
    
    args = parser.parse_args()
    
    server = LocalDevServer()
    server.backend_port = args.backend_port
    server.frontend_port = args.frontend_port
    
    if args.clean:
        print("🧹 清理端口占用...")
        server.cleanup_ports()
        print("✅ 清理完成")
        return
    
    # 启动服务
    success = server.run(args.mode)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
