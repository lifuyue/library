// 开发环境配置 (允许用 VITE_API_BASE_URL 覆盖，以便 local_dev 动态端口注入)
const DEV_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
export const development = {
  API_BASE_URL: DEV_BASE,
  UPLOAD_URL: `${DEV_BASE}/uploads`
}

// 生产环境配置
export const production = {
  API_BASE_URL: import.meta.env.VITE_API_BASE_URL || 'https://your-backend-name.onrender.com',
  UPLOAD_URL: `${import.meta.env.VITE_API_BASE_URL || 'https://your-backend-name.onrender.com'}/uploads`
}

// 根据环境变量自动选择配置
const config = import.meta.env.DEV ? development : production

export default config
