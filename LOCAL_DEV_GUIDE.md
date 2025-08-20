# CS素材库本地开发环境启动器

这里提供了三种启动本地开发服务的方式，可以根据你的系统和需求选择合适的方式。

## 🚀 启动方式

### 1. Python脚本 (推荐，跨平台)

```bash
# 启动全部服务（前端 + 后端）
python local_dev.py

# 仅启动后端服务
python local_dev.py --mode backend

# 仅启动前端服务  
python local_dev.py --mode frontend

# 自定义端口
python local_dev.py --backend-port 8001 --frontend-port 3001

# 清理端口占用
python local_dev.py --clean

# 查看帮助
python local_dev.py --help
```

### 2. Windows 批处理脚本

```cmd
REM 启动全部服务
start_local.bat

REM 仅启动后端服务
start_local.bat --backend-only

REM 仅启动前端服务
start_local.bat --frontend-only

REM 清理端口占用
start_local.bat --clean

REM 查看帮助
start_local.bat --help
```

### 3. Linux/Mac Shell脚本

```bash
# 给脚本执行权限
chmod +x start_local.sh

# 启动全部服务
./start_local.sh

# 仅启动后端服务
./start_local.sh --backend-only

# 仅启动前端服务
./start_local.sh --frontend-only

# 清理端口占用
./start_local.sh --clean

# 查看帮助
./start_local.sh --help
```

## ✨ 功能特性

### 🔍 智能检测
- ✅ 自动检测端口占用情况
- ✅ 自动检测项目依赖是否满足
- ✅ 自动安装缺失的前端依赖

### 🛠️ 进程管理
- ✅ 启动前自动清理端口占用的进程
- ✅ 支持优雅关闭和强制关闭
- ✅ 智能寻找可用端口

### 🎯 灵活启动
- ✅ 支持启动全部服务（前端+后端）
- ✅ 支持仅启动后端服务
- ✅ 支持仅启动前端服务
- ✅ 支持自定义端口号

### 📊 实时监控
- ✅ 实时显示服务启动状态
- ✅ 等待服务完全启动后再继续
- ✅ 超时检测和错误处理

## 🌐 默认访问地址

### 后端服务
- **API接口**: http://127.0.0.1:8000
- **API文档**: http://127.0.0.1:8000/docs  
- **健康检查**: http://127.0.0.1:8000/api/health

### 前端服务
- **前端应用**: http://localhost:3000

## ⚙️ 环境要求

### 必需依赖
- ✅ Python 3.7+ 
- ✅ Node.js 14+
- ✅ 已配置的虚拟环境 (.venv)
- ✅ 已安装的Python依赖包

### 项目结构要求
```
project/
├── .venv/                 # Python虚拟环境
├── backend/
│   ├── main.py           # FastAPI主文件
│   └── ...
├── frontend/
│   ├── package.json      # Node.js配置
│   ├── node_modules/     # Node.js依赖 (可选，会自动安装)
│   └── ...
├── local_dev.py          # Python启动脚本
├── start_local.bat       # Windows批处理脚本  
└── start_local.sh        # Linux/Mac Shell脚本
```

## 🐛 故障排除

### 端口占用问题
```bash
# 手动清理端口占用
python local_dev.py --clean

# 或者使用系统命令
# Windows:
netstat -ano | findstr :8000
taskkill /F /PID <进程ID>

# Linux/Mac:
lsof -ti:8000
kill -9 <进程ID>
```

### 依赖安装问题
```bash
# 重新安装Python依赖
pip install -r backend/requirements.txt

# 重新安装前端依赖
cd frontend && npm install
```

### 权限问题 (Linux/Mac)
```bash
# 给Shell脚本执行权限
chmod +x start_local.sh

# 如果端口需要管理员权限
sudo ./start_local.sh
```

## 💡 使用建议

1. **首次使用**：推荐使用Python脚本，它有最完整的错误检查和提示
2. **日常开发**：可以使用对应系统的脚本文件，启动更快
3. **CI/CD环境**：建议使用Python脚本，跨平台兼容性更好
4. **端口冲突**：脚本会自动寻找可用端口，无需手动处理

## 📞 技术支持

如果遇到问题，请检查：
1. 虚拟环境是否正确激活
2. Python和Node.js版本是否满足要求  
3. 项目依赖是否完整安装
4. 端口是否被其他程序占用

更多详细信息请查看项目的主要README文档。
