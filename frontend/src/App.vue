<script setup lang="ts">
import { RouterView } from 'vue-router'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const activeIndex = ref('1')

const logout = () => {
  authStore.clearAuth()
  router.push('/login')
}

onMounted(() => {
  authStore.initAuth()
})
</script>

<template>
  <div class="app">
    <!-- 顶部导航 -->
    <el-header class="header">
      <div class="header-content">
        <div class="logo">
          <h1>CS素材库</h1>
          <span class="subtitle">反恐精英道具教程素材集</span>
        </div>
        
        <el-menu
          mode="horizontal"
          :default-active="activeIndex"
          class="nav-menu"
          router
        >
          <el-menu-item index="/home">
            <el-icon><House /></el-icon>
            <span>首页</span>
          </el-menu-item>
          <el-menu-item index="/materials">
            <el-icon><Files /></el-icon>
            <span>素材库</span>
          </el-menu-item>
          <el-menu-item v-if="authStore.isAuthenticated" index="/upload">
            <el-icon><Upload /></el-icon>
            <span>上传素材</span>
          </el-menu-item>
        </el-menu>
        
        <div class="user-actions">
          <template v-if="authStore.isAuthenticated">
            <span class="welcome-text">欢迎，{{ authStore.user?.username }}</span>
            <el-button @click="logout">退出登录</el-button>
          </template>
          <template v-else>
            <el-button type="primary" plain @click="$router.push('/login')">登录</el-button>
            <el-button type="primary" @click="$router.push('/login')">注册</el-button>
          </template>
        </div>
      </div>
    </el-header>

    <!-- 主要内容区域 -->
    <el-main class="main-content">
      <RouterView />
    </el-main>

    <!-- 底部 -->
    <el-footer class="footer">
      <div class="footer-content">
        <p>&copy; 2024 CS素材库. 专注反恐精英道具教程分享</p>
      </div>
    </el-footer>
  </div>
</template>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background: #2c3e50;
  color: white;
  padding: 0;
  height: 70px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  padding: 0 20px;
}

.logo h1 {
  margin: 0;
  font-size: 24px;
  color: #fff;
}

.logo .subtitle {
  font-size: 12px;
  color: #bdc3c7;
}

.nav-menu {
  background: transparent;
  border: none;
}

.nav-menu .el-menu-item {
  color: #ecf0f1;
  border-bottom: 2px solid transparent;
}

.nav-menu .el-menu-item:hover {
  background-color: #34495e;
  color: #fff;
}

.nav-menu .el-menu-item.is-active {
  border-bottom-color: #3498db;
  color: #3498db;
}

.welcome-text {
  color: #ecf0f1;
  margin-right: 16px;
  font-size: 14px;
}

.main-content {
  flex: 1;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  padding: 20px;
}

.footer {
  background: #34495e;
  color: white;
  text-align: center;
  height: 60px;
  line-height: 60px;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
}
</style>
