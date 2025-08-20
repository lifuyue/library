<template>
  <div class="materials-view">
    <!-- 搜索和筛选 -->
    <div class="filters-section">
      <el-card>
        <el-row :gutter="20">
          <el-col :xs="24" :sm="12" :md="8">
            <el-input
              v-model="searchQuery"
              placeholder="搜索素材..."
              clearable
              @change="handleSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </el-col>
          <el-col :xs="24" :sm="6" :md="4">
            <el-select v-model="selectedCategory" placeholder="选择类别" clearable @change="handleFilter">
              <el-option
                v-for="category in categories"
                :key="category.value"
                :label="category.label"
                :value="category.value"
              />
            </el-select>
          </el-col>
          <el-col :xs="24" :sm="6" :md="4">
            <el-select v-model="selectedMap" placeholder="选择地图" clearable @change="handleFilter">
              <el-option
                v-for="map in maps"
                :key="map"
                :label="map"
                :value="map"
              />
            </el-select>
          </el-col>
        </el-row>
      </el-card>
    </div>

    <!-- 素材列表 -->
    <div class="materials-grid" v-loading="loading">
      <el-row :gutter="20">
        <el-col 
          :xs="24" :sm="12" :md="8" :lg="6" 
          v-for="material in materials" 
          :key="material.id"
        >
          <el-card class="material-card" shadow="hover" @click="viewMaterial(material.id)">
            <div class="material-image">
              <img 
                :src="material.thumbnail_path ? `/uploads/${material.thumbnail_path}` : '/placeholder.jpg'" 
                :alt="material.title"
                @error="handleImageError"
              />
              <div class="material-type">{{ getFileTypeLabel(material.file_type) }}</div>
              <div class="material-overlay">
                <el-button type="primary" circle>
                  <el-icon><View /></el-icon>
                </el-button>
              </div>
            </div>
            <div class="material-info">
              <h4>{{ material.title }}</h4>
              <p class="material-description">{{ material.description || '暂无描述' }}</p>
              <div class="material-meta">
                <el-tag size="small">{{ getCategoryLabel(material.category) }}</el-tag>
                <el-tag v-if="material.map_name" size="small" type="info">{{ material.map_name }}</el-tag>
              </div>
              <div class="material-stats">
                <span><el-icon><View /></el-icon> {{ material.views }}</span>
                <span><el-icon><Star /></el-icon> {{ material.likes }}</span>
                <span class="upload-time">{{ formatDate(material.created_at) }}</span>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 空状态 -->
      <el-empty v-if="!loading && materials.length === 0" description="暂无素材数据" />
    </div>

    <!-- 分页 -->
    <div class="pagination-section" v-if="total > 0">
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        :total="total"
        layout="prev, pager, next, jumper, total"
        @current-change="handlePageChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { materialsApi } from '@/api'
import type { Material, Category } from '@/types'

const router = useRouter()
const loading = ref(false)
const materials = ref<Material[]>([])
const categories = ref<Category[]>([])
const maps = ref<string[]>([])

// 搜索和筛选
const searchQuery = ref('')
const selectedCategory = ref('')
const selectedMap = ref('')

// 分页
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

const getCategoryLabel = (category: string) => {
  const labels: Record<string, string> = {
    smoke: '烟雾弹',
    flash: '闪光弹',
    he: '手雷',
    molotov: '燃烧瓶',
    position: '身位点位',
    strategy: '战术策略',
    other: '其他'
  }
  return labels[category] || category
}

const getFileTypeLabel = (type: string) => {
  const labels: Record<string, string> = {
    image: '图片',
    video: '视频',
    gif: 'GIF'
  }
  return labels[type] || type
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

const viewMaterial = (id: number) => {
  router.push(`/materials/${id}`)
}

const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.src = '/placeholder.jpg'
}

const loadMaterials = async () => {
  try {
    loading.value = true
    const params = {
      page: currentPage.value,
      size: pageSize.value,
      ...(searchQuery.value && { search: searchQuery.value }),
      ...(selectedCategory.value && { category: selectedCategory.value }),
      ...(selectedMap.value && { map_name: selectedMap.value })
    }
    
    const response = await materialsApi.getMaterials(params)
    materials.value = response.materials
    total.value = response.total
  } catch (error) {
    console.error('Failed to load materials:', error)
  } finally {
    loading.value = false
  }
}

const loadCategories = async () => {
  try {
    const response = await materialsApi.getCategories()
    categories.value = response.categories
  } catch (error) {
    console.error('Failed to load categories:', error)
  }
}

const loadMaps = async () => {
  try {
    const response = await materialsApi.getMaps()
    maps.value = response.maps
  } catch (error) {
    console.error('Failed to load maps:', error)
  }
}

const handleSearch = () => {
  currentPage.value = 1
  loadMaterials()
}

const handleFilter = () => {
  currentPage.value = 1
  loadMaterials()
}

const handlePageChange = () => {
  loadMaterials()
}

onMounted(() => {
  loadMaterials()
  loadCategories()
  loadMaps()
})
</script>

<style scoped>
.materials-view {
  padding: 20px 0;
}

.filters-section {
  margin-bottom: 30px;
}

.materials-grid {
  min-height: 400px;
}

.material-card {
  margin-bottom: 20px;
  cursor: pointer;
  transition: transform 0.3s ease;
  overflow: hidden;
}

.material-card:hover {
  transform: translateY(-5px);
}

.material-image {
  position: relative;
  height: 200px;
  overflow: hidden;
  background: #f5f5f5;
}

.material-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.material-card:hover .material-image img {
  transform: scale(1.05);
}

.material-type {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.material-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.material-card:hover .material-overlay {
  opacity: 1;
}

.material-info {
  padding: 16px;
}

.material-info h4 {
  margin: 0 0 8px 0;
  font-size: 16px;
  color: #2c3e50;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.material-description {
  color: #7f8c8d;
  font-size: 14px;
  margin-bottom: 12px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.material-meta {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.material-stats {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: #7f8c8d;
}

.material-stats span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.upload-time {
  font-size: 11px;
}

.pagination-section {
  display: flex;
  justify-content: center;
  margin-top: 40px;
}

@media (max-width: 768px) {
  .filters-section .el-col {
    margin-bottom: 10px;
  }
}
</style>
