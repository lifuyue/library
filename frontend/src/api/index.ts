import axios from 'axios'
import type { Material, MaterialResponse, Category } from '@/types'
import type { LoginForm, RegisterForm, AuthResponse, User } from '@/types/auth'
import type { AdminStats, AdminUser } from '@/types/admin'
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
  // 不能手动设置 multipart/form-data 头，否则 boundary 丢失导致后端解析不到字段 -> 422 Field required
  return api.post('/materials/upload', data)
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

// 管理员相关API
export const adminApi = {
  // 获取统计信息
  getStats: (): Promise<AdminStats> => {
    return api.get('/admin/stats')
  },

  // 获取待审核素材
  getPendingMaterials: (params?: {
    page?: number
    size?: number
  }): Promise<MaterialResponse> => {
    return api.get('/admin/materials/pending', { params })
  },

  // 审核通过素材
  approveMaterial: (id: number): Promise<{ message: string }> => {
    return api.post(`/admin/materials/${id}/approve`)
  },

  // 拒绝素材
  rejectMaterial: (id: number): Promise<{ message: string }> => {
    return api.post(`/admin/materials/${id}/reject`)
  },

  // 删除素材
  deleteMaterial: (id: number): Promise<{ message: string }> => {
    return api.delete(`/admin/materials/${id}`)
  },

  // 获取用户列表
  getUsers: (params?: {
    page?: number
    size?: number
  }): Promise<AdminUser[]> => {
    return api.get('/admin/users', { params })
  },

  // 切换用户激活状态
  toggleUserActive: (id: number): Promise<{ message: string }> => {
    return api.post(`/admin/users/${id}/toggle-active`)
  },

  // 切换用户管理员状态
  toggleUserAdmin: (id: number): Promise<{ message: string }> => {
    return api.post(`/admin/users/${id}/toggle-admin`)
  }
}
