<template>
  <div class="admin-users">
    <el-page-header content="用户管理" @back="router.push('/admin')" />
    
    <div class="users-content">
      <!-- 操作栏 -->
      <div class="toolbar">
        <div class="stats">
          <el-tag type="info">总用户: {{ users.length }}</el-tag>
          <el-tag type="success">活跃用户: {{ activeUsersCount }}</el-tag>
          <el-tag type="warning">管理员: {{ adminUsersCount }}</el-tag>
        </div>
        
        <el-button @click="loadUsers" :icon="Refresh" circle />
      </div>

      <!-- 用户表格 -->
      <div class="users-table" v-loading="loading">
        <el-table :data="users" stripe>
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="username" label="用户名" min-width="120" />
          <el-table-column prop="email" label="邮箱" min-width="200" />
          
          <el-table-column label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="row.is_active ? 'success' : 'danger'" size="small">
                {{ row.is_active ? '活跃' : '禁用' }}
              </el-tag>
            </template>
          </el-table-column>
          
          <el-table-column label="角色" width="100">
            <template #default="{ row }">
              <el-tag :type="row.is_admin ? 'warning' : 'info'" size="small">
                {{ row.is_admin ? '管理员' : '普通用户' }}
              </el-tag>
            </template>
          </el-table-column>
          
          <el-table-column label="注册时间" width="120">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>
          
          <el-table-column label="操作" width="200">
            <template #default="{ row }">
              <el-button-group>
                <el-button 
                  @click="toggleUserActive(row)"
                  :type="row.is_active ? 'warning' : 'success'"
                  size="small"
                  :loading="actionLoading[row.id]"
                >
                  {{ row.is_active ? '禁用' : '启用' }}
                </el-button>
                
                <el-button 
                  @click="toggleUserAdmin(row)"
                  :type="row.is_admin ? 'danger' : 'warning'"
                  size="small"
                  :loading="actionLoading[row.id]"
                  :disabled="row.id === currentUserId"
                >
                  {{ row.is_admin ? '取消管理员' : '设为管理员' }}
                </el-button>
              </el-button-group>
            </template>
          </el-table-column>
        </el-table>
        
        <!-- 空状态 -->
        <el-empty v-if="!loading && users.length === 0" description="暂无用户" />
      </div>
    </div>

    <!-- 用户详情对话框 -->
    <el-dialog v-model="detailVisible" title="用户详情" width="50%">
      <div v-if="selectedUser" class="user-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="用户ID">{{ selectedUser.id }}</el-descriptions-item>
          <el-descriptions-item label="用户名">{{ selectedUser.username }}</el-descriptions-item>
          <el-descriptions-item label="邮箱">{{ selectedUser.email }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="selectedUser.is_active ? 'success' : 'danger'">
              {{ selectedUser.is_active ? '活跃' : '禁用' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="角色">
            <el-tag :type="selectedUser.is_admin ? 'warning' : 'info'">
              {{ selectedUser.is_admin ? '管理员' : '普通用户' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="注册时间">{{ formatDate(selectedUser.created_at) }}</el-descriptions-item>
        </el-descriptions>
      </div>
      
      <template #footer>
        <el-button @click="detailVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import { adminApi } from '@/api'
import { useAuthStore } from '@/stores/auth'
import type { AdminUser } from '@/types/admin'

const router = useRouter()
const authStore = useAuthStore()

const loading = ref(false)
const users = ref<AdminUser[]>([])
const actionLoading = reactive<Record<number, boolean>>({})

// 用户详情
const detailVisible = ref(false)
const selectedUser = ref<AdminUser | null>(null)

// 当前用户ID（用于禁用自己的管理员操作）
const currentUserId = computed(() => authStore.user?.id)

// 统计信息
const activeUsersCount = computed(() => users.value.filter(u => u.is_active).length)
const adminUsersCount = computed(() => users.value.filter(u => u.is_admin).length)

// 格式化日期
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('zh-CN')
}

// 加载用户列表
const loadUsers = async () => {
  loading.value = true
  try {
    const response = await adminApi.getUsers()
    users.value = response
  } catch (error) {
    console.error('加载用户失败:', error)
    ElMessage.error('加载用户失败')
  } finally {
    loading.value = false
  }
}

// 切换用户激活状态
const toggleUserActive = async (user: AdminUser) => {
  const action = user.is_active ? '禁用' : '启用'
  
  try {
    await ElMessageBox.confirm(
      `确定要${action}用户 "${user.username}" 吗？`,
      `${action}用户`,
      { type: 'warning' }
    )
    
    actionLoading[user.id] = true
    await adminApi.toggleUserActive(user.id)
    ElMessage.success(`用户已${action}`)
    loadUsers()
  } catch (error) {
    if (error !== 'cancel') {
      console.error(`${action}用户失败:`, error)
      ElMessage.error(`${action}用户失败`)
    }
  } finally {
    actionLoading[user.id] = false
  }
}

// 切换用户管理员状态
const toggleUserAdmin = async (user: AdminUser) => {
  const action = user.is_admin ? '取消管理员权限' : '设为管理员'
  
  try {
    await ElMessageBox.confirm(
      `确定要${action}用户 "${user.username}" 吗？`,
      `${action}`,
      { type: 'warning' }
    )
    
    actionLoading[user.id] = true
    await adminApi.toggleUserAdmin(user.id)
    ElMessage.success(`已${action}`)
    loadUsers()
  } catch (error) {
    if (error !== 'cancel') {
      console.error(`${action}失败:`, error)
      ElMessage.error(`${action}失败`)
    }
  } finally {
    actionLoading[user.id] = false
  }
}

// 查看用户详情
const viewUserDetail = (user: AdminUser) => {
  selectedUser.value = user
  detailVisible.value = true
}

onMounted(() => {
  loadUsers()
})
</script>

<style scoped>
.admin-users {
  padding: 20px;
}

.users-content {
  margin-top: 20px;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.stats {
  display: flex;
  gap: 10px;
}

.users-table {
  min-height: 400px;
}

.user-detail {
  padding: 20px 0;
}

:deep(.el-table__row) {
  cursor: pointer;
}

:deep(.el-table__row:hover) {
  background-color: #f5f7fa;
}

:deep(.el-button-group .el-button) {
  margin: 0;
}
</style>
