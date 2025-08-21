<template>
  <div class="admin-materials">
    <el-page-header content="素材管理" @back="router.push('/admin')" />
    
    <div class="materials-content">
      <!-- 操作栏 -->
      <div class="toolbar">
        <el-radio-group v-model="currentTab" @change="handleTabChange">
          <el-radio-button label="pending">待审核 ({{ pendingCount }})</el-radio-button>
          <el-radio-button label="approved">已通过</el-radio-button>
          <el-radio-button label="all">全部素材</el-radio-button>
        </el-radio-group>
        
        <el-button @click="loadMaterials" :icon="Refresh" circle />
      </div>

      <!-- 素材列表 -->
      <div class="materials-list" v-loading="loading">
        <el-row :gutter="20">
          <el-col 
            :span="6" 
            v-for="material in materials" 
            :key="material.id"
            class="material-col"
          >
            <el-card class="material-card">
              <!-- 素材图片 -->
              <div class="material-image">
                <el-image 
                  :src="getImageUrl(material.thumbnail_path || material.file_path)"
                  :alt="material.title"
                  fit="cover"
                  lazy
                />
                <div class="material-overlay">
                  <el-button 
                    @click="previewMaterial(material)"
                    :icon="View"
                    circle
                    size="small"
                  />
                </div>
              </div>
              
              <!-- 素材信息 -->
              <div class="material-info">
                <h4 class="material-title">{{ material.title }}</h4>
                <p class="material-description">{{ material.description }}</p>
                <div class="material-meta">
                  <el-tag :type="getStatusType(material.is_approved)" size="small">
                    {{ getStatusText(material.is_approved) }}
                  </el-tag>
                  <span class="material-date">{{ formatDate(material.created_at) }}</span>
                </div>
              </div>
              
              <!-- 操作按钮 -->
              <div class="material-actions">
                <template v-if="!material.is_approved">
                  <el-button 
                    @click="approveMaterial(material.id)"
                    type="success"
                    size="small"
                    :icon="Check"
                    :loading="actionLoading[material.id]"
                  >
                    通过
                  </el-button>
                  <el-button 
                    @click="rejectMaterial(material.id)"
                    type="warning"
                    size="small"
                    :icon="Close"
                    :loading="actionLoading[material.id]"
                  >
                    拒绝
                  </el-button>
                </template>
                <el-button 
                  @click="deleteMaterial(material.id)"
                  type="danger"
                  size="small"
                  :icon="Delete"
                  :loading="actionLoading[material.id]"
                >
                  删除
                </el-button>
              </div>
            </el-card>
          </el-col>
        </el-row>
        
        <!-- 空状态 -->
        <el-empty v-if="!loading && materials.length === 0" description="暂无素材" />
      </div>

      <!-- 分页 -->
      <div class="pagination" v-if="total > 0">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[12, 24, 48]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @current-change="loadMaterials"
          @size-change="loadMaterials"
        />
      </div>
    </div>

    <!-- 预览对话框 -->
    <el-dialog v-model="previewVisible" title="素材预览" width="60%">
      <div v-if="selectedMaterial" class="preview-content">
        <div class="preview-image">
          <el-image 
            :src="getImageUrl(selectedMaterial?.file_path)"
            :alt="selectedMaterial?.title"
            fit="contain"
          />
        </div>
        <div class="preview-info">
          <h3>{{ selectedMaterial?.title }}</h3>
          <p>{{ selectedMaterial?.description }}</p>
          <div class="preview-meta">
            <p><strong>文件名：</strong>{{ selectedMaterial?.file_path?.split('/').pop() }}</p>
            <p><strong>文件大小：</strong>{{ formatFileSize(selectedMaterial?.file_size) }}</p>
            <p><strong>上传时间：</strong>{{ selectedMaterial?.created_at ? formatDate(selectedMaterial.created_at) : '未知' }}</p>
            <p><strong>状态：</strong>
              <el-tag :type="getStatusType(selectedMaterial?.is_approved ?? null)">
                {{ getStatusText(selectedMaterial?.is_approved ?? null) }}
              </el-tag>
            </p>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Refresh, 
  View, 
  Check, 
  Close, 
  Delete 
} from '@element-plus/icons-vue'
import { materialsApi, adminApi } from '@/api'
import config from '@/config/environment'
import type { Material } from '@/types'

const router = useRouter()

const currentTab = ref('pending')
const loading = ref(false)
const materials = ref<Material[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(12)
const pendingCount = ref(0)

const actionLoading = reactive<Record<number, boolean>>({})

// 预览相关
const previewVisible = ref(false)
const selectedMaterial = ref<Material | null>(null)

// 获取图片URL
const getImageUrl = (path: string | undefined) => {
  if (!path) return ''
  return `${config.UPLOAD_URL}/${path.replace(/\\/g, '/')}`
}

// 获取状态类型
const getStatusType = (isApproved: boolean | null) => {
  if (isApproved === true) return 'success'
  if (isApproved === false) return 'danger'
  return 'warning'
}

// 获取状态文本
const getStatusText = (isApproved: boolean | null) => {
  if (isApproved === true) return '已通过'
  if (isApproved === false) return '已拒绝'
  return '待审核'
}

// 格式化日期
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('zh-CN')
}

// 格式化文件大小
const formatFileSize = (bytes: number | undefined) => {
  if (!bytes) return '未知'
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(1024))
  return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i]
}

// 加载素材列表
const loadMaterials = async () => {
  loading.value = true
  try {
    let response
    if (currentTab.value === 'pending') {
      response = await adminApi.getPendingMaterials({
        page: currentPage.value,
        size: pageSize.value
      })
    } else {
      response = await materialsApi.getMaterials({
        page: currentPage.value,
        size: pageSize.value
      })
    }
    
    materials.value = response.materials
    total.value = response.total
    
    // 如果是待审核标签，更新计数
    if (currentTab.value === 'pending') {
      pendingCount.value = response.total
    }
  } catch (error) {
    console.error('加载素材失败:', error)
    ElMessage.error('加载素材失败')
  } finally {
    loading.value = false
  }
}

// 加载待审核数量
const loadPendingCount = async () => {
  try {
    const response = await adminApi.getPendingMaterials({ page: 1, size: 1 })
    pendingCount.value = response.total
  } catch (error) {
    console.error('加载待审核数量失败:', error)
  }
}

// 标签页切换
const handleTabChange = () => {
  currentPage.value = 1
  loadMaterials()
}

// 预览素材
const previewMaterial = (material: Material) => {
  selectedMaterial.value = material
  previewVisible.value = true
}

// 通过素材
const approveMaterial = async (id: number) => {
  actionLoading[id] = true
  try {
    await adminApi.approveMaterial(id)
    ElMessage.success('素材审核通过')
    loadMaterials()
    loadPendingCount()
  } catch (error) {
    console.error('审核失败:', error)
    ElMessage.error('审核失败')
  } finally {
    actionLoading[id] = false
  }
}

// 拒绝素材
const rejectMaterial = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定要拒绝这个素材吗？', '确认操作', {
      type: 'warning'
    })
    
    actionLoading[id] = true
    await adminApi.rejectMaterial(id)
    ElMessage.success('素材已拒绝')
    loadMaterials()
    loadPendingCount()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('拒绝失败:', error)
      ElMessage.error('拒绝失败')
    }
  } finally {
    actionLoading[id] = false
  }
}

// 删除素材
const deleteMaterial = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定要删除这个素材吗？删除后无法恢复。', '确认删除', {
      type: 'warning'
    })
    
    actionLoading[id] = true
    await adminApi.deleteMaterial(id)
    ElMessage.success('素材已删除')
    loadMaterials()
    loadPendingCount()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  } finally {
    actionLoading[id] = false
  }
}

onMounted(() => {
  loadMaterials()
  loadPendingCount()
})
</script>

<style scoped>
.admin-materials {
  padding: 20px;
}

.materials-content {
  margin-top: 20px;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.materials-list {
  min-height: 400px;
}

.material-col {
  margin-bottom: 20px;
}

.material-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.material-image {
  position: relative;
  height: 200px;
  overflow: hidden;
  border-radius: 4px;
}

.material-image .el-image {
  width: 100%;
  height: 100%;
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

.material-image:hover .material-overlay {
  opacity: 1;
}

.material-info {
  padding: 15px 0;
  flex: 1;
}

.material-title {
  margin: 0 0 8px 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.material-description {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: #606266;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.material-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.material-date {
  font-size: 12px;
  color: #909399;
}

.material-actions {
  padding-top: 15px;
  border-top: 1px solid #f0f0f0;
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.pagination {
  margin-top: 30px;
  text-align: center;
}

.preview-content {
  display: flex;
  gap: 20px;
}

.preview-image {
  flex: 1;
  max-height: 400px;
}

.preview-image .el-image {
  width: 100%;
  height: 100%;
}

.preview-info {
  flex: 1;
}

.preview-info h3 {
  margin: 0 0 15px 0;
  color: #303133;
}

.preview-info p {
  margin: 0 0 15px 0;
  color: #606266;
  line-height: 1.6;
}

.preview-meta {
  border-top: 1px solid #f0f0f0;
  padding-top: 15px;
}

.preview-meta p {
  margin: 0 0 8px 0;
  font-size: 14px;
}
</style>
