# CS素材库部署指南

## 目录结构
```
deploy/
├── netlify/          # Netlify 前端部署配置
│   └── README.md
├── render/           # Render 后端部署配置
│   └── README.md
└── docker/           # Docker 容器化部署配置
    ├── Dockerfile.backend
    ├── Dockerfile.frontend
    ├── nginx.conf
    └── docker-compose.yml
```

## 部署方案

### 方案一：Netlify + Render（推荐入门）
- **前端**: Netlify 静态网站托管
- **后端**: Render 云服务
- **优势**: 配置简单，免费额度充足，自动 HTTPS
- **适用**: 个人项目、快速原型

### 方案二：Docker + VPS（推荐长期）
- **前端**: Nginx 反向代理
- **后端**: FastAPI 容器
- **优势**: 完全控制，成本可控，性能更好
- **适用**: 生产环境、高并发需求

## 快速开始

### 1. Netlify + Render 部署

#### 步骤一：部署后端到 Render
1. 将代码推送到 GitHub
2. 访问 [Render](https://render.com) 并连接 GitHub
3. 创建 Web Service，使用 `render.yaml` 配置
4. 设置环境变量（参考 deploy/render/README.md）
5. 记录后端 URL（如：https://your-app.onrender.com）

#### 步骤二：部署前端到 Netlify
1. 访问 [Netlify](https://netlify.com) 并连接 GitHub
2. 选择仓库，Netlify 会自动检测 `netlify.toml`
3. 设置环境变量：
   ```
   VITE_API_BASE_URL=https://your-app.onrender.com
   ```
4. 部署完成，记录前端 URL

#### 步骤三：更新 CORS 配置
在 Render 环境变量中更新：
```
CORS_ORIGINS=https://your-site.netlify.app,http://localhost:3000
```

### 2. Docker 部署

#### 本地测试
```bash
cd deploy/docker
docker-compose up --build
```

#### VPS 部署
1. 安装 Docker 和 Docker Compose
2. 上传代码到服务器
3. 设置环境变量文件 `.env`
4. 运行部署命令：
   ```bash
   docker-compose up -d --build
   ```

## 环境变量配置

### 后端环境变量（PostgreSQL only）
```env
# 数据库（同步栈; psycopg 驱动）
DATABASE_URL=postgresql+psycopg://app:app@postgresql:5432/cslibrary

# JWT 安全
SECRET_KEY=your-very-secure-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=https://your-frontend.com,http://localhost:3000

# 文件上传
UPLOAD_DIR=uploads
MAX_FILE_SIZE=52428800

# 服务器
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=production
```

### 前端环境变量
```env
VITE_API_BASE_URL=https://your-backend.com
```

## 监控和维护

### 健康检查
- 后端：`GET /api/health`
- 前端：访问主页确认加载

### 日志查看
- Render：在 Dashboard 查看实时日志
- Docker：`docker-compose logs -f`

### 数据备份
- PostgreSQL：使用 pg_dump 备份
- 上传文件：定期备份 uploads 目录

## 扩展升级

### 从 Netlify+Render 迁移到 VPS
1. 备份数据库和文件
2. 设置 VPS 环境
3. 使用 Docker 部署
4. 更新域名 DNS
5. 测试功能完整性

### 性能优化
- 使用 CDN 加速静态资源
- 启用 Gzip 压缩
- 配置缓存策略

## 故障排除

### 常见问题
1. **CORS 错误**: 检查 CORS_ORIGINS 配置
2. **文件上传失败**: 检查上传目录权限
3. **数据库连接失败**: 检查 DATABASE_URL
4. **JWT 验证失败**: 检查 SECRET_KEY 配置

### 技术支持
- 查看各平台的详细文档
- 检查环境变量配置
- 验证网络连接和防火墙设置
