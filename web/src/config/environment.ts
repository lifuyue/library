// 开发环境配置 (允许用 VITE_API_BASE 覆盖，以便 local_dev 动态端口注入)
const DEV_BASE = import.meta.env.VITE_API_BASE || ''
export const development = {
  API_BASE_URL: DEV_BASE,
  UPLOAD_URL: `/uploads`
}

// 生产环境配置
export const production = {
  API_BASE_URL: import.meta.env.VITE_API_BASE || '',
  UPLOAD_URL: `/uploads`
}

// 根据环境变量自动选择配置
const config = import.meta.env.DEV ? development : production

export default config
