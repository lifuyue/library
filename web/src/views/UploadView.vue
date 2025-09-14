<template>
  <div class="upload-view">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>上传素材</h2>
          <p>分享你的CS道具教程，帮助更多玩家</p>
        </div>
      </template>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
        size="large"
      >
        <el-form-item label="标题" prop="title">
          <el-input
            v-model="form.title"
            placeholder="请输入素材标题"
            maxlength="100"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="类别" prop="category">
          <el-select v-model="form.category" placeholder="请选择道具类别" style="width: 100%">
            <el-option
              v-for="category in categories"
              :key="category.value"
              :label="category.label"
              :value="category.value"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="地图">
          <el-select v-model="form.map_name" placeholder="请选择地图（可选）" clearable style="width: 100%">
            <el-option
              v-for="map in maps"
              :key="map"
              :label="map"
              :value="map"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="描述">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="4"
            placeholder="请描述这个道具的用途、投掷方法等..."
            maxlength="500"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="标签">
          <el-input
            v-model="form.tags"
            placeholder="用逗号分隔标签，如：一键烟，长箱烟，CT家"
            maxlength="200"
          />
        </el-form-item>

        <el-form-item label="文件" prop="file">
          <el-upload
            ref="uploadRef"
            class="upload-demo"
            drag
            :auto-upload="false"
            :limit="1"
            :on-change="handleFileChange"
            :before-upload="beforeUpload"
            accept="image/*,video/*,.gif"
          >
            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div class="el-upload__text">
              将文件拖到此处，或<em>点击上传</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                支持 jpg/png/gif/mp4/mov/avi 格式，文件大小不超过 50MB
              </div>
            </template>
          </el-upload>
          
          <!-- 文件预览 -->
          <div v-if="filePreview" class="file-preview">
            <div class="preview-container">
              <img v-if="isImage" :src="filePreview" alt="预览图" />
              <video v-else-if="isVideo" :src="filePreview" controls></video>
              <div class="file-info">
                <p><strong>文件名:</strong> {{ selectedFile?.name }}</p>
                <p><strong>文件大小:</strong> {{ formatFileSize(selectedFile?.size || 0) }}</p>
                <p><strong>文件类型:</strong> {{ selectedFile?.type }}</p>
              </div>
            </div>
          </div>
        </el-form-item>

        <el-form-item>
          <el-button 
            type="primary" 
            :loading="uploading" 
            :disabled="uploading"
            @click="submitForm"
            size="large"
          >
            <el-icon v-if="!uploading"><Upload /></el-icon>
            <el-icon v-else class="is-loading"><Loading /></el-icon>
            {{ uploading ? '正在上传素材...' : '提交素材' }}
          </el-button>
          <el-button @click="resetForm" :disabled="uploading">重置</el-button>
          
          <!-- 上传进度提示 -->
          <div v-if="uploading" class="upload-tip">
            <el-text type="info" size="small">
              <el-icon class="is-loading"><Loading /></el-icon>
              文件上传中，请耐心等待...
            </el-text>
          </div>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, type FormInstance, type UploadFile } from 'element-plus'
import { Upload, Loading } from '@element-plus/icons-vue'
import { materialsApi } from '@/api'
import type { Category, UploadForm } from '@/types'

const router = useRouter()
const formRef = ref<FormInstance>()
const uploadRef = ref()
const uploading = ref(false)
const categories = ref<Category[]>([])
const maps = ref<string[]>([])

// 本地回退常量（后端不可用或超时使用）
const DEFAULT_CATEGORIES: Category[] = [
  { value: 'smoke', label: '烟雾弹' },
  { value: 'flash', label: '闪光弹' },
  { value: 'he', label: '手雷' },
  { value: 'molotov', label: '燃烧瓶' },
  { value: 'position', label: '身位点位' },
  { value: 'strategy', label: '战术策略' },
  { value: 'other', label: '其他' }
]
const DEFAULT_MAPS: string[] = [
  'dust2', 'mirage', 'inferno', 'cache', 'overpass',
  'train', 'cobblestone', 'nuke', 'vertigo', 'ancient'
]

// 文件相关
const selectedFile = ref<File>()
const filePreview = ref('')
const isImage = ref(false)
const isVideo = ref(false)

// 表单数据
const form = reactive<UploadForm>({
  title: '',
  category: '',
  description: '',
  map_name: '',
  tags: '',
  file: undefined
})

// 表单验证规则
const rules = {
  title: [
    { required: true, message: '请输入标题', trigger: 'blur' },
    { min: 2, max: 100, message: '标题长度在 2 到 100 个字符', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择类别', trigger: 'change' }
  ],
  file: [
    { 
      validator: (_rule: any, _value: any, callback: (err?: Error) => void) => {
        if (!selectedFile.value) {
          callback(new Error('请选择文件'))
        } else {
          callback()
        }
      },
      trigger: 'change'
    }
  ]
}

const formatFileSize = (size: number) => {
  if (size < 1024) return size + ' B'
  if (size < 1024 * 1024) return (size / 1024).toFixed(2) + ' KB'
  return (size / (1024 * 1024)).toFixed(2) + ' MB'
}

const handleFileChange = (file: UploadFile) => {
  if (file.raw) {
    selectedFile.value = file.raw
    form.file = file.raw // 同步到表单模型，供校验使用
    
    // 创建预览
    const reader = new FileReader()
    reader.onload = (e) => {
      filePreview.value = e.target?.result as string
      
      // 判断文件类型
      const type = file.raw?.type || ''
      isImage.value = type.startsWith('image/')
      isVideo.value = type.startsWith('video/')
    }
    reader.readAsDataURL(file.raw)

    // 触发文件字段单独校验（避免已选文件还提示“请选择文件”）
    formRef.value?.validateField('file')
  } else {
    // 清空
    selectedFile.value = undefined
    form.file = undefined
  }
}

const beforeUpload = (file: File) => {
  const isValidType = /\.(jpg|jpeg|png|gif|mp4|mov|avi|webm)$/i.test(file.name)
  const isValidSize = file.size / 1024 / 1024 < 50

  if (!isValidType) {
    ElMessage.error('不支持的文件格式!')
    return false
  }
  if (!isValidSize) {
    ElMessage.error('文件大小不能超过 50MB!')
    return false
  }
  return true
}

const submitForm = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    if (!selectedFile.value) {
      ElMessage.error('请选择文件')
      return
    }
    try {
      uploading.value = true
      
      // 显示上传开始消息
      const uploadingMessage = ElMessage({
        message: '正在上传素材，请稍候...',
        type: 'info',
        duration: 0, // 不自动关闭
        showClose: false
      })
      
      const formData = new FormData()
      formData.append('title', form.title)
      formData.append('category', form.category)
      formData.append('file', selectedFile.value)
      if (form.description) formData.append('description', form.description)
      if (form.map_name) formData.append('map_name', form.map_name)
      if (form.tags) formData.append('tags', form.tags)
      
      const result = await materialsApi.uploadMaterial(formData)
      
      // 关闭上传中消息
      uploadingMessage.close()
      
      // 显示成功消息
      ElMessage({
        message: `素材《${form.title}》上传成功！正在跳转到详情页...`,
        type: 'success',
        duration: 3000,
        showClose: true
      })
      
      // 延迟跳转，让用户看到成功消息
      setTimeout(() => {
        router.push(`/materials/${result.id}`)
      }, 1500)
      
    } catch (error: any) {
      console.error('Upload failed:', error)
      let message = '上传失败，请检查网络连接或重试'
      // FastAPI 常见错误字段 detail
      if (error?.response?.data) {
        const data = error.response.data
        if (typeof data === 'string') {
          message = `上传失败：${data}`
        } else if (data.detail) {
          if (Array.isArray(data.detail)) {
            // Pydantic 验证错误数组
            message = data.detail.map((d: any) => d.msg || d.detail || JSON.stringify(d)).join('; ')
          } else if (typeof data.detail === 'string') {
            message = data.detail
          } else if (typeof data.detail === 'object') {
            message = JSON.stringify(data.detail)
          }
        } else {
          // 兜底序列化对象避免 [object Object]
            message = JSON.stringify(data)
        }
      } else if (error?.message) {
        message = error.message
      }
      ElMessage.error(`上传失败：${message}`)
    } finally {
      uploading.value = false
    }
  })
}

const resetForm = () => {
  formRef.value?.resetFields()
  selectedFile.value = undefined
  form.file = undefined
  filePreview.value = ''
  isImage.value = false
  isVideo.value = false
  uploadRef.value?.clearFiles()
}

const loadCategories = async (retry = 0) => {
  try {
    const response = await materialsApi.getCategories()
    if (response?.categories?.length) {
      categories.value = response.categories
    } else {
      throw new Error('empty categories response')
    }
  } catch (error) {
    console.warn('加载类别失败，使用本地回退:', error)
    categories.value = DEFAULT_CATEGORIES
    // 首次失败尝试一次重试（避免偶发冷启动）
    if (retry === 0) {
      setTimeout(() => loadCategories(1), 1500)
    }
  }
}

const loadMaps = async (retry = 0) => {
  try {
    const response = await materialsApi.getMaps()
    if (response?.maps?.length) {
      maps.value = response.maps
    } else {
      throw new Error('empty maps response')
    }
  } catch (error) {
    console.warn('加载地图失败，使用本地回退:', error)
    maps.value = DEFAULT_MAPS
    if (retry === 0) {
      setTimeout(() => loadMaps(1), 1500)
    }
  }
}

onMounted(() => {
  loadCategories()
  loadMaps()
})
</script>

<style scoped>
.upload-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.card-header h2 {
  margin: 0 0 8px 0;
  color: #2c3e50;
}

.card-header p {
  margin: 0;
  color: #7f8c8d;
  font-size: 14px;
}

.upload-demo {
  width: 100%;
}

.file-preview {
  margin-top: 20px;
  padding: 20px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  background: #fafafa;
}

.preview-container img,
.preview-container video {
  max-width: 100%;
  max-height: 300px;
  border-radius: 4px;
  margin-bottom: 16px;
}

.file-info p {
  margin: 4px 0;
  font-size: 14px;
  color: #606266;
}

.el-form-item {
  margin-bottom: 24px;
}

.upload-tip {
  margin-top: 12px;
  padding: 8px 12px;
  background: #f0f9ff;
  border: 1px solid #bae7ff;
  border-radius: 4px;
  text-align: center;
}

.upload-tip .el-icon {
  margin-right: 6px;
}

@media (max-width: 768px) {
  .upload-view {
    padding: 10px;
  }
  
  .preview-container img,
  .preview-container video {
    max-height: 200px;
  }
}
</style>
