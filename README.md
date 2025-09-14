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
- **PostgreSQL** - 关系型数据库
- **Uvicorn** - ASGI服务器

## 项目结构

```
library/
├── backend/                 # 后端 FastAPI 应用
│   ├── alembic/            # 数据库迁移
│   │   └── versions/       # 迁移版本文件
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据模型
│   │   └── schemas/        # Pydantic模式
│   ├── scripts/            # 实用脚本
│   ├── uploads/            # 上传文件存储
│   ├── alembic.ini         # Alembic配置
│   ├── main.py            # 应用入口
│   └── requirements.txt   # Python依赖
├── web/                    # 前端 Vue 应用
│   ├── src/
│   │   ├── api/           # API接口
│   │   ├── components/    # 组件
│   │   ├── views/         # 页面视图
│   │   ├── types/         # TypeScript类型
│   │   └── assets/        # 静态资源
│   ├── package.json       # Node.js依赖
│   └── vite.config.ts     # Vite配置
├── packages/               # 共用模块（预留）
├── miniprogram/            # 小程序（预留）
└── README.md              # 项目说明
```

## 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- npm 或 yarn

### 配置环境变量

```bash
cp .env.example .env
```

本地开发可将 `.env.example` 复制为 `.env` 提供默认变量；CI 和生产环境通过运行时注入环境变量，无需 `.env` 文件。后端在开发模式下会尝试加载 `.env`（若存在），生产环境仅读取进程环境变量。

> **前端 API 地址配置**
> - **容器开发模式**：确保 `.env` 或 `web/.env.development` 中 `VITE_API_BASE=http://backend:8000`，再通过 `docker compose up` 一键启动。
> - **本地直连模式**：若直接访问本机后端，请设置 `VITE_API_BASE=http://127.0.0.1:8000`，并在后端开启允许该来源的 CORS。

### Docker Compose 启动（PostgreSQL）

```bash
# 构建并启动全部服务
docker compose up -d --build

# 或使用 Makefile
make dev-build
```

首次启动时容器会等待数据库就绪并执行 `alembic upgrade head`，确保表结构与默认管理员存在。通过日志查看迁移结果：

```bash
docker compose logs -f backend
```

应用启动后可访问 `http://localhost:8000/healthz` 进行检查。

### 使用 Makefile（推荐）

如果已安装 Docker 与 Docker Compose（v2），可以使用根目录下的 `Makefile` 快速启动：

```bash
# 开发环境（前台运行，显示日志）
make dev

# 开发环境（后台运行）
make dev-up-d

# 重新构建并启动开发环境
make dev-build

# 查看开发环境日志
make dev-logs

# 进入容器
make sh-backend
make sh-frontend

# 生产环境（后台运行）
make prod-up

# 停止
make dev-down
make prod-down
```

更多命令请运行 `make help` 查看。

新增一键 Docker 命令：

```bash
make docker-build && make docker-up
# 查看日志 / 停止
make docker-logs
make docker-down
```

Windows 用户指南（不再提供 .bat/.cmd）：
- 使用 WSL 或 Git Bash 执行上述命令；
- 或在 PowerShell 中等价运行：
  - 后端开发：`python -m uvicorn backend.main:app --reload`
  - 前端开发：`cd web; npm run dev`
  - Docker：`docker compose up -d`

### 开发环境启动

#### 启动后端（方式一：run_server 脚本）

```bash
# Windows (PowerShell)
python backend/run_server.py
```

#### 启动后端（方式二：直接运行 main.py）

```bash
python backend/main.py
```

#### 启动后端（方式三：uvicorn 手动）

```bash
cd backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

> 已移除旧的 dev.py / start-dev.* 脚本，改用更清晰的方式。

**1. 后端启动**

```bash
# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 安装依赖（首次运行）
pip install -r backend/requirements.txt

# 运行数据库迁移（首次运行或更新后）
cd backend
alembic upgrade head

# 启动后端服务
python run_server.py
```

**2. 前端启动**

```bash
# 在新的终端窗口中
cd web

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

### 环境变量说明（节选）

- `SECRET_KEY`：JWT 密钥（必改）
- `ALGORITHM`：JWT 算法（默认 HS256）
- `ACCESS_TOKEN_EXPIRE_MINUTES`：令牌过期（默认 60）
- `UPLOAD_DIR`：上传目录（默认 `uploads`，Compose 映射为命名卷）
- `MAX_FILE_SIZE`：上传大小限制（默认 50MB）

### 健康检查

- 后端：`GET /healthz` 返回 200
  - Docker Compose 内置 `healthcheck`，容器会等待依赖就绪

### 生产部署（Route B：Nginx 反向代理，单一入口）

- 统一对外公开 `nginx:80`，Nginx 将：
  - `/api/*` 代理到后端 `cslibrary-backend:8000`
  - `/uploads/*` 代理到后端 `cslibrary-backend:8000`
  - 其余路径代理到前端 `cslibrary-frontend:80`
- 前端使用相对路径请求 API（`/api/...`），避免出现 `/api/api`。

验证命令：
```bash
docker compose up -d --build
docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
curl -i http://127.0.0.1/
curl -i http://127.0.0.1/healthz
```

## 数据库迁移

项目使用 **Alembic** 管理数据库 schema 变更，确保多环境一致性和可回滚性。

### 首次设置或更新后

```bash
cd backend
alembic upgrade head
```

### 创建新迁移（开发时）

```bash
cd backend
# 自动检测模型变更并生成迁移
alembic revision --autogenerate -m "描述变更内容"
# 手动检查生成的迁移文件
# 应用迁移
alembic upgrade head
```

### 常用命令

```bash
# 查看当前迁移状态
alembic current

# 查看迁移历史
alembic history

# 回滚到上一个版本
alembic downgrade -1

# 回滚到指定版本
alembic downgrade <revision_id>
```

## 管理员账号说明

## 管理员账号说明

系统使用 **Alembic 迁移**自动创建默认管理员账户。运行 `alembic upgrade head` 时会检查并创建：

- 用户名: `admin`
- 密码: `admin123`
- 邮箱: `admin@example.com`

默认值可通过环境变量覆盖：

```
ADMIN_DEFAULT_USERNAME=admin
ADMIN_DEFAULT_EMAIL=admin@example.com
ADMIN_DEFAULT_PASSWORD=admin123
```

### 重置 / 修改管理员

提供了脚本 `backend/scripts/reset_admin.py`：

```bash
python backend/scripts/reset_admin.py --force --password 新密码123
```

参数：
- `--username` 覆盖用户名（默认取环境变量或 admin）
- `--email` 覆盖邮箱
- `--password` 设定新密码
- `--force` 若已存在则强制更新密码/邮箱/权限

**安全提示**：生产环境务必修改默认密码，并设置强随机 `SECRET_KEY`。

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
- is_admin: 是否管理员
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
- 数据库：使用 PostgreSQL
- 文件存储：可配置对象存储服务

## 常见问题

- 数据库连接失败：确认环境变量 `DATABASE_URL` 与 Compose 配置一致，并确保 `db` 服务健康。
- 权限问题：卷挂载目录需具备读写权限。
- 重复迁移：若 `alembic` 报错，检查并清理 `alembic_version` 表后重试。

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
