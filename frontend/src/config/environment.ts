// 开发环境配置
export const development = {
  API_BASE_URL: 'http://localhost:8000',
  UPLOAD_URL: 'http://localhost:8000/uploads'
}

// 生产环境配置
export const production = {
  API_BASE_URL: import.meta.env.VITE_API_BASE_URL || 'https://your-backend-name.onrender.com',
  UPLOAD_URL: `${import.meta.env.VITE_API_BASE_URL || 'https://your-backend-name.onrender.com'}/uploads`
}

// 根据环境变量自动选择配置
const config = import.meta.env.DEV ? development : production

export default config
