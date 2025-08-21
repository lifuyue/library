<template>
  <div class="admin-dashboard">
    <el-page-header content="管理员面板" />
    
    <div class="dashboard-content">
      <!-- 统计卡片 -->
      <el-row :gutter="20" class="stats-row">
        <el-col :span="6">
          <el-card class="stats-card">
            <div class="stats-content">
              <div class="stats-icon">
                <el-icon size="40">
                  <Document />
                </el-icon>
              </div>
              <div class="stats-info">
                <div class="stats-number">{{ stats.totalMaterials }}</div>
                <div class="stats-label">总素材数</div>
              </div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="6">
          <el-card class="stats-card">
            <div class="stats-content">
              <div class="stats-icon">
                <el-icon size="40" color="#67C23A">
                  <Check />
                </el-icon>
              </div>
              <div class="stats-info">
                <div class="stats-number">{{ stats.approvedMaterials }}</div>
                <div class="stats-label">已通过</div>
              </div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="6">
          <el-card class="stats-card">
            <div class="stats-content">
              <div class="stats-icon">
                <el-icon size="40" color="#E6A23C">
                  <Clock />
                </el-icon>
              </div>
              <div class="stats-info">
                <div class="stats-number">{{ stats.pendingMaterials }}</div>
                <div class="stats-label">待审核</div>
              </div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="6">
          <el-card class="stats-card">
            <div class="stats-content">
              <div class="stats-icon">
                <el-icon size="40" color="#409EFF">
                  <User />
                </el-icon>
              </div>
              <div class="stats-info">
                <div class="stats-number">{{ stats.totalUsers }}</div>
                <div class="stats-label">用户总数</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 管理菜单 -->
      <el-row :gutter="20" class="menu-row">
        <el-col :span="12">
          <el-card class="menu-card" @click="router.push('/admin/materials')">
            <div class="menu-content">
              <el-icon size="60" color="#409EFF">
                <Folder />
              </el-icon>
              <h3>素材管理</h3>
              <p>审核、删除和管理素材内容</p>
              <el-badge :value="stats.pendingMaterials" :hidden="stats.pendingMaterials === 0" class="menu-badge">
                <span></span>
              </el-badge>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="12">
          <el-card class="menu-card" @click="router.push('/admin/users')">
            <div class="menu-content">
              <el-icon size="60" color="#67C23A">
                <UserFilled />
              </el-icon>
              <h3>用户管理</h3>
              <p>管理用户权限和状态</p>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Document, Check, Clock, User, Folder, UserFilled } from '@element-plus/icons-vue'
import { adminApi } from '@/api'
import type { AdminStats } from '@/types/admin'

const router = useRouter()

const stats = ref<AdminStats>({
  totalMaterials: 0,
  approvedMaterials: 0,
  pendingMaterials: 0,
  totalUsers: 0,
  activeUsers: 0
})

const loading = ref(false)

const loadStats = async () => {
  loading.value = true
  try {
    const response = await adminApi.getStats()
    stats.value = response
  } catch (error) {
    console.error('加载统计数据失败:', error)
    ElMessage.error('加载统计数据失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.admin-dashboard {
  padding: 20px;
}

.dashboard-content {
  margin-top: 20px;
}

.stats-row {
  margin-bottom: 30px;
}

.stats-card {
  cursor: default;
}

.stats-content {
  display: flex;
  align-items: center;
  gap: 15px;
}

.stats-icon {
  color: #409EFF;
}

.stats-info {
  text-align: left;
}

.stats-number {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
  line-height: 1;
}

.stats-label {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}

.menu-row {
  margin-top: 20px;
}

.menu-card {
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.menu-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.menu-content {
  text-align: center;
  padding: 20px;
  position: relative;
}

.menu-content h3 {
  margin: 15px 0 10px 0;
  color: #303133;
}

.menu-content p {
  color: #909399;
  margin: 0;
  font-size: 14px;
}

.menu-badge {
  position: absolute;
  top: 10px;
  right: 10px;
}
</style>
