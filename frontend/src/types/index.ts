export interface Material {
  id: number
  title: string
  description?: string
  category: string
  map_name?: string
  file_path: string
  file_type: string
  file_size?: number
  thumbnail_path?: string
  tags?: string
  views: number
  likes: number
  uploader_id: number
  is_approved: boolean
  created_at: string
  updated_at: string
  uploader: User
}

export interface User {
  id: number
  username: string
  email: string
  is_active: boolean
  created_at: string
}

export interface MaterialResponse {
  materials: Material[]
  total: number
  page: number
  size: number
}

export interface Category {
  value: string
  label: string
}

export interface UploadForm {
  title: string
  category: string
  description?: string
  map_name?: string
  tags?: string
  file?: File
}
