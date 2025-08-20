import axios from 'axios'
import type { Material, MaterialResponse, Category } from '@/types'
import type { LoginForm, RegisterForm, AuthResponse, User } from '@/types/auth'
import config from '@/config/environment'

const api = axios.create({
  baseURL: `${config.API_BASE_URL}/api`,
  timeout: 10000,
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 添加 Authorization header
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    if (error.response?.status === 401) {
      // Token 过期或无效，清除本地存储
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

// 素材相关API
export const materialsApi = {
  // 获取素材列表
  getMaterials: (params?: {
    page?: number
    size?: number
    category?: string
    map_name?: string
    search?: string
  }): Promise<MaterialResponse> => {
    return api.get('/materials', { params })
  },

  // 获取单个素材详情
  getMaterial: (id: number): Promise<Material> => {
    return api.get(`/materials/${id}`)
  },

  // 点赞素材
  likeMaterial: (id: number): Promise<{ likes: number }> => {
    return api.post(`/materials/${id}/like`)
  },

  // 上传素材
  uploadMaterial: (data: FormData): Promise<Material> => {
    return api.post('/materials/upload', data, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  // 获取类别列表
  getCategories: (): Promise<{ categories: Category[] }> => {
    return api.get('/materials/categories/list')
  },

  // 获取地图列表
  getMaps: (): Promise<{ maps: string[] }> => {
    return api.get('/materials/maps/list')
  }
}

export default api

// 认证相关API
export const authApi = {
  // 用户登录
  login: (credentials: LoginForm): Promise<AuthResponse> => {
    return api.post('/users/login', credentials)
  },

  // 用户注册
  register: (userData: RegisterForm): Promise<User> => {
    return api.post('/users/register', userData)
  },

  // 获取当前用户信息
  getCurrentUser: (): Promise<User> => {
    return api.get('/users/me')
  }
}
