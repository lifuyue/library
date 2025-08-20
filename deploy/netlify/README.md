# Netlify 部署配置

## 配置步骤

### 1. 准备工作
- 确保你的项目已推送到 GitHub/GitLab/Bitbucket
- 在 Netlify 注册账号并连接代码仓库

### 2. 环境变量配置
在 Netlify 控制台的 Site settings > Environment variables 中添加：
```
VITE_API_BASE_URL=https://your-backend-name.onrender.com
```

### 3. 构建设置
Netlify 会自动检测 `netlify.toml` 配置，无需手动设置

### 4. 自定义域名（可选）
在 Domain settings 中添加自定义域名

## 配置说明

### 构建配置
- **Publish directory**: `frontend/dist`
- **Build command**: 自动安装依赖并构建前端项目
- **Node.js version**: 18

### 重定向规则
1. API 代理：将 `/api/*` 请求转发到后端服务器
2. 静态资源：将 `/uploads/*` 请求转发到后端文件服务
3. SPA 支持：所有其他路由重定向到 `index.html`

### 环境变量
- 生产环境使用 Render 后端 URL
- 预览部署和分支部署同样指向生产后端

## 注意事项
1. 部署前请先部署后端到 Render
2. 将 `your-backend-name` 替换为实际的 Render 应用名称
3. 确保后端 CORS 设置包含 Netlify 域名
