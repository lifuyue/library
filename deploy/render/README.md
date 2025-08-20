# Render 部署配置

## 配置步骤

### 1. 准备工作
- 确保你的项目已推送到 GitHub
- 在 Render 注册账号并连接 GitHub

### 2. 创建 Web Service
1. 在 Render Dashboard 点击 "New Web Service"
2. 选择你的 GitHub 仓库
3. 使用以下配置：
   - **Name**: cs-library-backend
   - **Environment**: Python 3
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && python main.py`
   - **Plan**: Free

### 3. 环境变量配置
在 Environment 标签页添加：
```
DATABASE_URL=sqlite:///./cs_library.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
CORS_ORIGINS=https://your-frontend-name.netlify.app,http://localhost:3000
```

### 4. 持久化存储配置
1. 在 Settings > Disks 添加磁盘：
   - **Name**: cs-library-storage
   - **Mount Path**: `/app/backend/uploads`
   - **Size**: 1GB

### 5. 自动部署
启用 Auto-Deploy，每次推送到 main 分支自动部署

## 配置说明

### 服务类型
- **Web Service**: HTTP API 服务
- **Environment**: Python 3
- **Plan**: Free（足够初期使用）

### 构建和启动
- 自动安装 requirements.txt 中的依赖
- 启动 FastAPI 应用（uvicorn 服务器）

### 数据库
- 使用 SQLite 文件数据库
- 数据文件保存在持久化磁盘中
- 免费方案包含基本存储

### 文件存储
- 用户上传的文件保存在 `/uploads` 目录
- 通过持久化磁盘确保文件不丢失

## 注意事项
1. 免费方案有一定限制（每月 750 小时运行时间）
2. 服务休眠后重启可能需要几秒钟
3. 确保 CORS_ORIGINS 包含前端域名
4. 部署完成后更新前端的 API_BASE_URL
