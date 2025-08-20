<template>
  <div class="material-detail-view" v-loading="loading">
    <el-card v-if="material">
      <template #header>
        <div class="detail-header">
          <div class="header-content">
            <h1>{{ material.title }}</h1>
            <div class="material-meta">
              <el-tag size="large">{{ getCategoryLabel(material.category) }}</el-tag>
              <el-tag v-if="material.map_name" size="large" type="info">{{ material.map_name }}</el-tag>
              <span class="upload-info">
                由 {{ material.uploader.username }} 于 {{ formatDate(material.created_at) }} 上传
              </span>
            </div>
          </div>
          <div class="header-actions">
            <el-button @click="$router.back()">
              <el-icon><ArrowLeft /></el-icon>
              返回
            </el-button>
          </div>
        </div>
      </template>

      <div class="material-content">
        <el-row :gutter="24">
          <!-- 媒体内容 -->
          <el-col :xs="24" :lg="16">
            <div class="media-container">
              <img 
                v-if="material.file_type === 'image' || material.file_type === 'gif'"
                :src="`/uploads/${material.file_path}`"
                :alt="material.title"
                class="material-image"
                @error="handleImageError"
              />
              <video 
                v-else-if="material.file_type === 'video'"
                :src="`/uploads/${material.file_path}`"
                controls
                class="material-video"
              >
                您的浏览器不支持视频播放
              </video>
              
              <div class="media-info">
                <div class="file-type">{{ getFileTypeLabel(material.file_type) }}</div>
                <div class="file-size" v-if="material.file_size">
                  {{ formatFileSize(material.file_size) }}
                </div>
              </div>
            </div>
          </el-col>

          <!-- 详细信息 -->
          <el-col :xs="24" :lg="8">
            <div class="info-panel">
              <div class="stats-section">
                <h3>统计信息</h3>
                <div class="stats-grid">
                  <div class="stat-item">
                    <el-icon><View /></el-icon>
                    <span class="stat-value">{{ material.views }}</span>
                    <span class="stat-label">浏览</span>
                  </div>
                  <div class="stat-item">
                    <el-icon><Star /></el-icon>
                    <span class="stat-value">{{ material.likes }}</span>
                    <span class="stat-label">点赞</span>
                  </div>
                </div>
              </div>

              <div class="description-section" v-if="material.description">
                <h3>描述</h3>
                <p class="description-text">{{ material.description }}</p>
              </div>

              <div class="tags-section" v-if="material.tags">
                <h3>标签</h3>
                <div class="tags-container">
                  <el-tag 
                    v-for="tag in material.tags.split(',')" 
                    :key="tag.trim()"
                    size="small"
                    class="tag-item"
                  >
                    {{ tag.trim() }}
                  </el-tag>
                </div>
              </div>

              <div class="actions-section">
                <el-button type="primary" @click="likeMaterial" :disabled="liked">
                  <el-icon><Star /></el-icon>
                  {{ liked ? '已点赞' : '点赞' }}
                </el-button>
                <el-button @click="downloadFile">
                  <el-icon><Download /></el-icon>
                  下载
                </el-button>
                <el-button @click="shareFile">
                  <el-icon><Share /></el-icon>
                  分享
                </el-button>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
    </el-card>

    <!-- 相关素材推荐 -->
    <el-card class="related-materials" v-if="relatedMaterials.length > 0">
      <template #header>
        <h3>相关素材</h3>
      </template>
      <el-row :gutter="16">
        <el-col 
          :xs="24" :sm="12" :md="6" 
          v-for="related in relatedMaterials" 
          :key="related.id"
        >
          <el-card class="related-card" shadow="hover" @click="viewRelated(related.id)">
            <div class="related-image">
              <img 
                :src="related.thumbnail_path ? `/uploads/${related.thumbnail_path}` : '/placeholder.jpg'"
                :alt="related.title"
                @error="handleImageError"
              />
            </div>
            <div class="related-info">
              <h4>{{ related.title }}</h4>
              <p>{{ getCategoryLabel(related.category) }}</p>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { materialsApi } from '@/api'
import type { Material } from '@/types'

const route = useRoute()
const router = useRouter()
const loading = ref(false)
const material = ref<Material>()
const relatedMaterials = ref<Material[]>([])
const liked = ref(false)

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

const formatFileSize = (size: number) => {
  if (size < 1024) return size + ' B'
  if (size < 1024 * 1024) return (size / 1024).toFixed(2) + ' KB'
  return (size / (1024 * 1024)).toFixed(2) + ' MB'
}

const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.src = '/placeholder.jpg'
}

const loadMaterial = async () => {
  try {
    loading.value = true
    const id = Number(route.params.id)
    material.value = await materialsApi.getMaterial(id)
    
    // 加载相关素材
    if (material.value) {
      const response = await materialsApi.getMaterials({
        category: material.value.category,
        size: 4
      })
      relatedMaterials.value = response.materials.filter(m => m.id !== material.value?.id)
    }
  } catch (error) {
    console.error('Failed to load material:', error)
    ElMessage.error('加载素材失败')
  } finally {
    loading.value = false
  }
}

const likeMaterial = async () => {
  if (!liked.value && material.value) {
    try {
      const resp = await materialsApi.likeMaterial(material.value.id)
      material.value.likes = resp.likes
      liked.value = true
      ElMessage.success('点赞成功!')
    } catch (e) {
      ElMessage.error('点赞失败')
    }
  }
}

const downloadFile = () => {
  if (material.value) {
    const link = document.createElement('a')
    link.href = `/uploads/${material.value.file_path}`
    link.download = material.value.title
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }
}

const shareFile = async () => {
  if (navigator.share && material.value) {
    try {
      await navigator.share({
        title: material.value.title,
        text: material.value.description || '',
        url: window.location.href
      })
    } catch (error) {
      // 如果不支持原生分享，复制链接到剪贴板
      navigator.clipboard.writeText(window.location.href)
      ElMessage.success('链接已复制到剪贴板')
    }
  } else {
    navigator.clipboard.writeText(window.location.href)
    ElMessage.success('链接已复制到剪贴板')
  }
}

const viewRelated = (id: number) => {
  router.push(`/materials/${id}`)
  loadMaterial() // 重新加载新的素材
}

onMounted(() => {
  loadMaterial()
})
</script>

<style scoped>
.material-detail-view {
  padding: 20px 0;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
}

.header-content h1 {
  margin: 0 0 16px 0;
  font-size: 32px;
  color: #2c3e50;
}

.material-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.upload-info {
  color: #7f8c8d;
  font-size: 14px;
}

.media-container {
  position: relative;
  text-align: center;
  background: #f8f9fa;
  border-radius: 8px;
  overflow: hidden;
}

.material-image,
.material-video {
  width: 100%;
  max-height: 600px;
  object-fit: contain;
}

.media-info {
  position: absolute;
  top: 16px;
  right: 16px;
  display: flex;
  gap: 8px;
}

.file-type,
.file-size {
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.info-panel {
  padding: 20px;
  background: #fafafa;
  border-radius: 8px;
}

.info-panel h3 {
  margin: 0 0 16px 0;
  color: #2c3e50;
  font-size: 18px;
}

.stats-section {
  margin-bottom: 30px;
}

.stats-grid {
  display: flex;
  gap: 20px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px;
  background: white;
  border-radius: 8px;
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #3498db;
}

.stat-label {
  font-size: 14px;
  color: #7f8c8d;
}

.description-section {
  margin-bottom: 30px;
}

.description-text {
  line-height: 1.6;
  color: #606266;
  margin: 0;
}

.tags-section {
  margin-bottom: 30px;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-item {
  margin: 0;
}

.actions-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.actions-section .el-button {
  width: 100%;
}

.related-materials {
  margin-top: 30px;
}

.related-card {
  cursor: pointer;
  transition: transform 0.3s ease;
  margin-bottom: 16px;
}

.related-card:hover {
  transform: translateY(-5px);
}

.related-image {
  height: 120px;
  overflow: hidden;
  background: #f5f5f5;
}

.related-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.related-info {
  padding: 12px;
}

.related-info h4 {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: #2c3e50;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.related-info p {
  margin: 0;
  font-size: 12px;
  color: #7f8c8d;
}

@media (max-width: 768px) {
  .detail-header {
    flex-direction: column;
  }
  
  .header-content h1 {
    font-size: 24px;
  }
  
  .material-meta {
    justify-content: flex-start;
  }
  
  .stats-grid {
    flex-direction: column;
  }
  
  .actions-section {
    flex-direction: column;
  }
}
</style>
