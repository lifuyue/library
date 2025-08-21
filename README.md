# CS素材库 - 反恐精英道具教程素材集

一个基于 Vue 3 + FastAPI 的现代化素材库网站，专注于反恐精英（CS）道具教程的分享和管理。

## 项目特色

- 🎯 **专业定位**: 专注于CS道具教程，包括烟雾弹、闪光弹、手雷等各类道具投掷技巧
- 🗺️ **多地图支持**: 覆盖dust2、mirage、inferno等热门竞技地图
- 📱 **响应式设计**: 完美适配桌面端和移动端
- 🔍 **智能搜索**: 支持按类别、地图、关键词快速查找
- 📤 **便捷上传**: 支持图片、视频、GIF格式的素材上传
- 👥 **社区驱动**: 用户自由分享，共同构建知识库

## 技术栈

### 前端
- **Vue 3** - 渐进式JavaScript框架
- **TypeScript** - 类型安全的JavaScript超集
- **Element Plus** - Vue 3组件库
- **Vite** - 下一代前端构建工具
- **Pinia** - Vue状态管理
- **Vue Router** - 官方路由管理器

### 后端
- **FastAPI** - 现代、快速的Python Web框架
- **SQLAlchemy** - Python SQL工具包和ORM
- **Alembic** - 数据库迁移工具
- **SQLite** - 轻量级数据库
- **Uvicorn** - ASGI服务器

## 项目结构

```
library/
├── backend/                 # 后端 FastAPI 应用
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据模型
│   │   └── schemas/        # Pydantic模式
│   ├── uploads/            # 上传文件存储
│   ├── main.py            # 应用入口
│   └── requirements.txt   # Python依赖
├── frontend/               # 前端 Vue 应用
│   ├── src/
│   │   ├── api/           # API接口
│   │   ├── components/    # 组件
│   │   ├── views/         # 页面视图
│   │   ├── types/         # TypeScript类型
│   │   └── assets/        # 静态资源
│   ├── package.json       # Node.js依赖
│   └── vite.config.ts     # Vite配置
└── README.md              # 项目说明
```

## 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- npm 或 yarn

### 开发环境启动

#### 方式一：Python启动脚本（推荐）

```bash
# 简单一键启动
python dev.py
```

#### 方式二：批处理脚本

**Windows:**
```bash
# 双击运行或在命令行中执行
start-dev.bat
```

**Linux/Mac:**
```bash
# 给脚本执行权限并运行
chmod +x start-dev.sh
./start-dev.sh
```

#### 方式三：手动启动

**1. 后端启动**

```bash
# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 安装依赖（首次运行）
pip install -r backend/requirements.txt

# 启动后端服务
cd backend
python run_server.py
```

**2. 前端启动**

```bash
# 在新的终端窗口中
cd frontend

# 安装依赖（首次运行）
npm install

# 启动前端开发服务器
npm run dev
```

### 访问地址

启动成功后，你可以访问：

- **前端应用**: http://localhost:3000
- **后端API**: http://127.0.0.1:8000  
- **API文档**: http://127.0.0.1:8000/docs

## API文档

启动后端服务后，访问以下地址查看API文档：

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 主要功能

### 素材浏览
- 网格布局展示素材
- 支持分页浏览
- 按类别和地图筛选
- 关键词搜索功能

### 素材上传
- 拖拽上传界面
- 支持多种文件格式
- 实时预览功能
- 表单验证

### 素材详情
- 高清图片/视频展示
- 详细信息显示
- 相关素材推荐
- 点赞和下载功能

## 数据库模型

### 用户表 (users)
- id: 主键
- username: 用户名
- email: 邮箱
- hashed_password: 加密密码
- is_active: 是否激活
- created_at: 创建时间

### 素材表 (materials)
- id: 主键
- title: 标题
- description: 描述
- category: 类别（smoke, flash, he, molotov等）
- map_name: 地图名称
- file_path: 文件路径
- file_type: 文件类型
- thumbnail_path: 缩略图路径
- views: 浏览次数
- likes: 点赞数
- uploader_id: 上传者ID
- is_approved: 是否审核通过

## 部署说明

### 开发环境
- 后端：`python main.py`
- 前端：`npm run dev`

### 生产环境
- 后端：使用 Gunicorn 或 Uvicorn 部署
- 前端：`npm run build` 后部署静态文件
- 数据库：可切换到 PostgreSQL 或 MySQL
- 文件存储：可配置对象存储服务

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

- 项目主页: [GitHub Repository]
- 问题反馈: [GitHub Issues]

---

**注意**: 这是一个学习和演示项目，请根据实际需求进行调整和优化。
