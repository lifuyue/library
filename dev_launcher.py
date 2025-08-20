#!/usr/bin/env python3
"""
CS素材库启动选择器
提供交互式的启动选项选择
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """打印欢迎横幅"""
    print("=" * 60)
    print("🎯 CS素材库开发环境启动选择器")
    print("=" * 60)
    print()

def print_menu():
    """打印菜单选项"""
    print("请选择启动模式：")
    print()
    print("1. 🚀 启动完整开发环境 (前端 + 后端)")
    print("2. 🔧 仅启动后端服务 (API + 数据库)")
    print("3. 🌐 仅启动前端服务 (Vue.js 应用)")
    print("4. 🧹 清理端口占用")
    print("5. 📖 查看启动说明")
    print("6. ❌ 退出")
    print()

def get_user_choice():
    """获取用户选择"""
    while True:
        try:
            choice = input("请输入选项编号 (1-6): ").strip()
            if choice in ['1', '2', '3', '4', '5', '6']:
                return int(choice)
            else:
                print("⚠️  请输入有效的选项编号 (1-6)")
        except KeyboardInterrupt:
            print("\n\n👋 再见!")
            sys.exit(0)
        except Exception:
            print("⚠️  输入错误，请重试")

def run_script(script_args):
    """运行启动脚本"""
    project_root = Path(__file__).parent
    python_exe = project_root / ".venv" / "Scripts" / "python.exe"
    
    if not python_exe.exists():
        # 尝试Linux/Mac路径
        python_exe = project_root / ".venv" / "bin" / "python"
        
    if not python_exe.exists():
        print("❌ 虚拟环境未找到，请先创建虚拟环境")
        return False
    
    local_dev_script = project_root / "local_dev.py"
    if not local_dev_script.exists():
        print("❌ 启动脚本未找到")
        return False
    
    try:
        cmd = [str(python_exe), str(local_dev_script)] + script_args
        subprocess.run(cmd)
        return True
    except KeyboardInterrupt:
        print("\n🛑 用户中断")
        return True
    except Exception as e:
        print(f"❌ 运行错误: {e}")
        return False

def show_guide():
    """显示启动说明"""
    print("\n" + "=" * 60)
    print("📖 CS素材库启动说明")
    print("=" * 60)
    print()
    print("🎯 项目架构：")
    print("  • 前端：Vue.js + Element Plus (端口: 3000)")
    print("  • 后端：FastAPI + SQLAlchemy (端口: 8000)")
    print("  • 数据库：SQLite")
    print()
    print("🚀 启动选项说明：")
    print("  1. 完整环境 - 同时启动前端和后端，适合全栈开发")
    print("  2. 仅后端 - 只启动API服务，适合API开发和测试")
    print("  3. 仅前端 - 只启动前端应用，适合UI开发")
    print("  4. 清理端口 - 清理被占用的8000和3000端口")
    print()
    print("🌐 访问地址：")
    print("  • 前端应用: http://localhost:3000")
    print("  • 后端API: http://127.0.0.1:8000")
    print("  • API文档: http://127.0.0.1:8000/docs")
    print("  • 健康检查: http://127.0.0.1:8000/api/health")
    print()
    print("💡 使用提示：")
    print("  • 首次运行会自动安装前端依赖")
    print("  • 服务启动后按Ctrl+C可以安全停止")
    print("  • 如果端口被占用，脚本会自动寻找可用端口")
    print("  • 支持热重载，修改代码后自动刷新")
    print()
    print("🐛 故障排除：")
    print("  • 端口占用：选择选项4清理端口")
    print("  • 依赖问题：检查虚拟环境和npm依赖")
    print("  • 权限问题：以管理员身份运行")
    print()
    input("按任意键返回主菜单...")

def main():
    """主函数"""
    print_banner()
    
    while True:
        print_menu()
        choice = get_user_choice()
        
        if choice == 1:
            print("\n🚀 启动完整开发环境...")
            if not run_script(["--mode", "full"]):
                input("\n按任意键返回主菜单...")
                
        elif choice == 2:
            print("\n🔧 启动后端服务...")
            if not run_script(["--mode", "backend"]):
                input("\n按任意键返回主菜单...")
                
        elif choice == 3:
            print("\n🌐 启动前端服务...")
            if not run_script(["--mode", "frontend"]):
                input("\n按任意键返回主菜单...")
                
        elif choice == 4:
            print("\n🧹 清理端口占用...")
            if not run_script(["--clean"]):
                input("\n按任意键返回主菜单...")
            else:
                print("✅ 端口清理完成")
                input("\n按任意键返回主菜单...")
                
        elif choice == 5:
            show_guide()
            
        elif choice == 6:
            print("\n👋 感谢使用CS素材库开发环境!")
            sys.exit(0)
        
        print()  # 空行分隔

if __name__ == "__main__":
    main()
