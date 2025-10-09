<template>
  <div class="market-news">
    <h3>📰 코스피 최신 뉴스</h3>
    
    <div v-if="loading" class="loading">
      <p>뉴스를 불러오는 중...</p>
    </div>

    <div v-else-if="error" class="error-state">
      <p>{{ error }}</p>
      <button @click="fetchNews" class="retry-btn">다시 시도</button>
    </div>

    <div v-else-if="news.length === 0" class="empty-state">
      <p>뉴스가 없습니다</p>
    </div>

    <div v-else class="news-list">
      <a 
        v-for="(item, index) in news" 
        :key="index"
        :href="item.link"
        target="_blank"
        rel="noopener noreferrer"
        class="news-item"
      >
        <div class="news-title">{{ item.title }}</div>
        <div class="news-meta">
          <span class="source">{{ item.source }}</span>
          <span class="time">{{ formatTime(item.published) }}</span>
        </div>
      </a>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const API_BASE = 'http://localhost:8000/api'

const news = ref([])
const loading = ref(false)
const error = ref('')

const formatTime = (dateString) => {
  if (!dateString) return ''
  
  try {
    const date = new Date(dateString)
    const now = new Date()
    const diff = Math.floor((now - date) / 1000)
    
    if (diff < 3600) {
      return `${Math.floor(diff / 60)}분 전`
    } else if (diff < 86400) {
      return `${Math.floor(diff / 3600)}시간 전`
    } else if (diff < 604800) {
      return `${Math.floor(diff / 86400)}일 전`
    } else {
      return date.toLocaleDateString('ko-KR')
    }
  } catch {
    return ''
  }
}

const fetchNews = async () => {
  loading.value = true
  error.value = ''

  try {
    console.log('뉴스 조회 시작...')
    const response = await axios.get(`${API_BASE}/stock/market-news`, {
      params: { limit: 10 }
    })

    console.log('뉴스 응답:', response.data)

    if (response.data.success) {
      news.value = response.data.news
      console.log(`${news.value.length}개 뉴스 로드 완료`)
    } else {
      error.value = '뉴스를 불러오는데 실패했습니다'
    }
  } catch (err) {
    console.error('뉴스 조회 실패:', err)
    error.value = '뉴스를 불러오는데 실패했습니다'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  console.log('MarketNews 컴포넌트 마운트됨 - 뉴스 자동 로드')
  fetchNews()
})

defineExpose({ fetchNews })
</script>

<style scoped>
.market-news {
  background: #1e1e1e;
  border-radius: 10px;
  padding: 20px;
}

h3 {
  color: #4CAF50;
  font-size: 18px;
  margin-bottom: 15px;
  border-bottom: 2px solid #333;
  padding-bottom: 10px;
}

.loading,
.error-state,
.empty-state {
  text-align: center;
  padding: 40px;
  color: #888;
}

.retry-btn {
  margin-top: 15px;
  padding: 10px 20px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.retry-btn:hover {
  background: #45a049;
}

.news-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.news-item {
  background: #2d2d2d;
  border: 2px solid #444;
  border-radius: 8px;
  padding: 15px;
  text-decoration: none;
  transition: all 0.3s;
  display: block;
}

.news-item:hover {
  border-color: #4CAF50;
  background: #353535;
  transform: translateX(5px);
}

.news-title {
  color: white;
  font-size: 14px;
  line-height: 1.5;
  margin-bottom: 8px;
  font-weight: 500;
}

.news-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
}

.source {
  color: #4CAF50;
  font-weight: 600;
}

.time {
  color: #888;
}
</style>
