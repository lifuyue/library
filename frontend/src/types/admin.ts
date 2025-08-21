export interface AdminStats {
  totalMaterials: number
  approvedMaterials: number
  pendingMaterials: number
  totalUsers: number
  activeUsers: number
}

export interface PendingMaterial {
  id: number
  title: string
  description?: string
  category: string
  map_name?: string
  file_path: string
  file_type: string
  thumbnail_path?: string
  uploader: {
    id: number
    username: string
    email: string
  }
  created_at: string
}

export interface AdminUser {
  id: number
  username: string
  email: string
  is_active: boolean
  is_admin: boolean
  created_at: string
  materials_count: number
}
