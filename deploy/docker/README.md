# PostgreSQL 部署指南

## 快速启动

1. 进入部署目录：
```bash
cd deploy/docker
```

2. 配置环境变量（生产环境必须修改）：
```bash
cp .env.deploy .env.deploy.local
# 编辑 .env.deploy.local，修改密码和密钥
```

3. 使用部署脚本启动：
```bash
./deploy.sh
```

或手动启动：
```bash
docker compose up -d --build
```

4. 查看启动状态：
```bash
docker compose ps
docker compose logs -f
```

## 数据库管理

使用 `db-manage.sh` 脚本管理数据库：

```bash
# 查看数据库状态
./db-manage.sh status

# 连接数据库
./db-manage.sh connect

# 备份数据库
./db-manage.sh backup

# 恢复数据库
./db-manage.sh restore backup_20250830_120000.sql

# 执行迁移
./db-manage.sh migrate

# 重置数据库 (危险操作)
./db-manage.sh reset

# 查看数据库日志
./db-manage.sh logs
```

## 生产环境安全配置

⚠️ **生产环境部署前必须修改以下配置：**

1. **修改数据库密码：**
   - `POSTGRES_PASSWORD`
   - `DATABASE_URL` 中的密码部分

2. **修改 JWT 密钥：**
   - `SECRET_KEY` 使用长随机字符串

3. **修改默认管理员：**
   - `ADMIN_DEFAULT_USERNAME`
   - `ADMIN_DEFAULT_EMAIL`
   - `ADMIN_DEFAULT_PASSWORD`

4. **配置 CORS：**
   - `CORS_ORIGINS` 设置为实际的前端域名

## 数据管理

### 使用脚本管理
```bash
# 备份数据库
./db-manage.sh backup

# 恢复数据库  
./db-manage.sh restore backup_file.sql

# 连接数据库
./db-manage.sh connect
```

### 手动管理
```bash
# 备份数据库
docker exec cs-library-postgres pg_dump -U cs_user cs_library > backup_$(date +%Y%m%d_%H%M%S).sql

# 恢复数据库
docker exec -i cs-library-postgres psql -U cs_user cs_library < backup.sql

# 查看数据库连接
docker exec -it cs-library-postgres psql -U cs_user cs_library
```

## 故障排除

### 查看服务状态
```bash
docker compose ps
```

### 查看后端日志
```bash
docker compose logs backend
```

### 查看数据库日志
```bash
docker compose logs db
```

### 重启服务
```bash
docker compose restart backend
```

### 完全重建
```bash
docker compose down -v
docker compose up -d --build
```

## 端口说明

- **8000**: 后端 API 服务
- **80**: 前端服务（如果启用）
- **5432**: PostgreSQL 数据库（仅容器内网络访问）

## 文件结构

```
deploy/docker/
├── docker-compose.yml      # 容器编排配置
├── Dockerfile.backend      # 后端镜像构建
├── .env.deploy            # 环境变量模板
└── README.md              # 本文档
```

## 注意事项

1. 数据库数据存储在 Docker 卷 `pg_data` 中
2. 上传文件存储在 Docker 卷 `backend_uploads` 中  
3. 生产环境建议使用外部 PostgreSQL 服务
4. 建议定期备份数据库和上传文件
