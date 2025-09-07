import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

import App from './App.vue'
import router from './router'

const app = createApp(App)

// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(createPinia())
app.use(router)
app.use(ElementPlus)

window.addEventListener('error', (e) => {
  console.error('Global error:', e.error || e.message)
})

window.addEventListener('unhandledrejection', (e) => {
  console.error('Unhandled rejection:', e.reason)
})

async function checkBackend() {
  try {
    const res = await fetch('/api/healthz')
    if (!res.ok) throw new Error(res.statusText)
    console.info('Backend health check OK')
  } catch (err) {
    console.error('Backend unreachable', err)
    const banner = document.createElement('div')
    banner.textContent = 'Backend API unreachable'
    banner.style.position = 'fixed'
    banner.style.top = '0'
    banner.style.left = '0'
    banner.style.right = '0'
    banner.style.background = '#c00'
    banner.style.color = '#fff'
    banner.style.padding = '8px'
    banner.style.textAlign = 'center'
    document.body.appendChild(banner)
  }
}

checkBackend()

app.mount('#app')
