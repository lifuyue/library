<template>
  <div class="home-view">
    <!-- 英雄区域 -->
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">CS素材库</h1>
        <p class="hero-subtitle">最全面的反恐精英道具教程素材集</p>
        <p class="hero-description">
          分享和发现最新的CS道具投掷技巧、身位点位、战术策略。
          <br>
          助你在游戏中取得优势，提升竞技水平。
        </p>
        <div class="hero-actions">
          <el-button type="primary" size="large" @click="$router.push('/materials')">
            <el-icon><Search /></el-icon>
            浏览素材
          </el-button>
          <el-button type="success" size="large" @click="$router.push('/upload')">
            <el-icon><Upload /></el-icon>
            上传素材
          </el-button>
        </div>
      </div>
    </div>

    <!-- 特色功能 -->
    <div class="features-section">
      <div class="container">
        <h2 class="section-title">核心功能</h2>
        <el-row :gutter="20">
          <el-col :xs="24" :sm="12" :md="8" v-for="feature in features" :key="feature.title">
            <el-card class="feature-card" shadow="hover">
              <div class="feature-icon">
                <el-icon size="40"><component :is="feature.icon" /></el-icon>
              </div>
              <h3>{{ feature.title }}</h3>
              <p>{{ feature.description }}</p>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </div>

    <!-- 最新素材 -->
    <div class="recent-materials">
      <div class="container">
        <h2 class="section-title">最新素材</h2>
        <el-row :gutter="20" v-loading="loading">
          <el-col :xs="24" :sm="12" :md="6" v-for="material in recentMaterials" :key="material.id">
            <el-card class="material-card" shadow="hover" @click="viewMaterial(material.id)">
              <div class="material-image">
                <img
                  :src="resolveThumb(material)"
                  :alt="material.title"
                  @error="handleImageError"
                />
                <div class="material-type">{{ getFileTypeLabel(material.file_type) }}</div>
              </div>
              <div class="material-info">
                <h4>{{ material.title }}</h4>
                <p class="material-meta">
                  <el-tag size="small">{{ getCategoryLabel(material.category) }}</el-tag>
                  <span v-if="material.map_name" class="map-name">{{ material.map_name }}</span>
                </p>
                <div class="material-stats">
                  <span><el-icon><View /></el-icon> {{ material.views }}</span>
                  <span><el-icon><Star /></el-icon> {{ material.likes }}</span>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
        
        <div class="view-more" v-if="recentMaterials.length > 0">
          <el-button type="primary" @click="$router.push('/materials')">
            查看更多素材
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { materialsApi } from '@/api'
import type { Material } from '@/types'
import config from '@/config/environment'

const router = useRouter()
const loading = ref(false)
const recentMaterials = ref<Material[]>([])

const features = [
  {
    icon: 'Files',
    title: '丰富素材',
    description: '包含烟雾弹、闪光弹、手雷等各类道具投掷教程'
  },
  {
    icon: 'Location',
    title: '多地图支持',
    description: '覆盖dust2、mirage、inferno等热门竞技地图'
  },
  {
    icon: 'Share',
    title: '社区分享',
    description: '玩家自由上传分享，共同构建知识库'
  },
  {
    icon: 'Star',
    title: '精选内容',
    description: '审核机制确保内容质量，为你推荐最佳素材'
  },
  {
    icon: 'Search',
    title: '智能搜索',
    description: '支持按类别、地图、关键词快速查找所需素材'
  },
  {
    icon: 'TrendCharts',
    title: '数据统计',
    description: '浏览量、点赞数等数据帮助发现热门内容'
  }
]

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

const viewMaterial = (id: number) => {
  router.push(`/materials/${id}`)
}

const PLACEHOLDER = '/placeholder.jpg'

const resolveThumb = (m: Material) => {
  if (m.thumbnail_path) return `${config.UPLOAD_URL}/${m.thumbnail_path}`
  if (m.file_path) return `${config.UPLOAD_URL}/${m.file_path}`
  return PLACEHOLDER
}

const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  if (img.src.endsWith(PLACEHOLDER)) return
  img.src = PLACEHOLDER
}

const loadRecentMaterials = async () => {
  try {
    loading.value = true
    const response = await materialsApi.getMaterials({ page: 1, size: 8 })
    recentMaterials.value = response.materials
  } catch (error) {
    console.error('Failed to load recent materials:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadRecentMaterials()
})
</script>

<style scoped>
.home-view {
  min-height: 100vh;
}

.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 100px 20px;
  text-align: center;
}

.hero-title {
  font-size: 48px;
  font-weight: bold;
  margin-bottom: 16px;
}

.hero-subtitle {
  font-size: 24px;
  margin-bottom: 24px;
  opacity: 0.9;
}

.hero-description {
  font-size: 16px;
  line-height: 1.6;
  margin-bottom: 40px;
  opacity: 0.8;
}

.hero-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

.features-section {
  padding: 80px 20px;
  background: #f8f9fa;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.section-title {
  text-align: center;
  font-size: 32px;
  margin-bottom: 50px;
  color: #2c3e50;
}

.feature-card {
  text-align: center;
  padding: 30px 20px;
  margin-bottom: 20px;
  border: none;
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-icon {
  color: #3498db;
  margin-bottom: 20px;
}

.feature-card h3 {
  font-size: 20px;
  margin-bottom: 16px;
  color: #2c3e50;
}

.feature-card p {
  color: #7f8c8d;
  line-height: 1.6;
}

.recent-materials {
  padding: 80px 20px;
}

.material-card {
  cursor: pointer;
  margin-bottom: 20px;
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

.material-info {
  padding: 16px;
}

.material-info h4 {
  margin: 0 0 8px 0;
  font-size: 16px;
  color: #2c3e50;
}

.material-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.map-name {
  font-size: 12px;
  color: #7f8c8d;
}

.material-stats {
  display: flex;
  gap: 16px;
  font-size: 12px;
  color: #7f8c8d;
}

.material-stats span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.view-more {
  text-align: center;
  margin-top: 40px;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 36px;
  }
  
  .hero-subtitle {
    font-size: 20px;
  }
  
  .hero-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .hero-actions .el-button {
    width: 200px;
  }
}
</style>
