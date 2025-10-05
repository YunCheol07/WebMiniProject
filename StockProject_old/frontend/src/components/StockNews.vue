<template>
  <div class="stock-news">
    <h3>📰 관련 뉴스</h3>
    
    <div v-if="loading" class="loading">
      <p>뉴스를 불러오는 중...</p>
    </div>

    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
    </div>

    <div v-else-if="newsList.length === 0" class="no-news">
      <p>뉴스가 없습니다.</p>
    </div>

    <div v-else class="news-list">
      <div 
        v-for="(news, index) in newsList" 
        :key="index"
        class="news-item"
      >
        <div class="news-header">
          <span class="news-source">{{ news.source }}</span>
          <span class="news-date">{{ formatDate(news.published) }}</span>
        </div>
        <a 
          :href="news.link" 
          target="_blank" 
          rel="noopener noreferrer"
          class="news-title"
        >
          {{ news.title }}
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, defineProps } from 'vue';
import axios from 'axios';

const props = defineProps({
  stockCode: String,
  stockName: String
});

const API_BASE = 'http://localhost:8000/api';

const newsList = ref([]);
const loading = ref(false);
const error = ref('');

// 뉴스 가져오기
const fetchNews = async () => {
  if (!props.stockCode) return;
  
  loading.value = true;
  error.value = '';
  
  try {
    const response = await axios.get(`${API_BASE}/stock/news/${props.stockCode}`);
    
    if (response.data.success) {
      newsList.value = response.data.news;
    } else {
      error.value = '뉴스를 불러올 수 없습니다.';
    }
  } catch (err) {
    console.error('뉴스 조회 실패:', err);
    error.value = '뉴스 조회 중 오류가 발생했습니다.';
  } finally {
    loading.value = false;
  }
};

// 날짜 포맷팅
const formatDate = (dateString) => {
  if (!dateString) return '';
  
  try {
    const date = new Date(dateString);
    const now = new Date();
    const diff = Math.floor((now - date) / 1000 / 60); // 분 단위
    
    if (diff < 60) {
      return `${diff}분 전`;
    } else if (diff < 1440) {
      return `${Math.floor(diff / 60)}시간 전`;
    } else {
      return date.toLocaleDateString('ko-KR', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    }
  } catch (e) {
    return dateString;
  }
};

// stockCode 변경 시 뉴스 다시 로드
watch(() => props.stockCode, () => {
  if (props.stockCode) {
    fetchNews();
  }
}, { immediate: true });

// 외부에서 호출 가능하도록 expose
defineExpose({ fetchNews });
</script>

<style scoped>
.stock-news {
  background: #1e1e1e;
  padding: 20px;
  border-radius: 10px;
  margin-top: 20px;
}

h3 {
  color: #4CAF50;
  margin-bottom: 20px;
  font-size: 20px;
}

.loading,
.error,
.no-news {
  text-align: center;
  padding: 40px;
  color: #888;
}

.error {
  color: #f44336;
}

.news-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.news-item {
  background: #2d2d2d;
  padding: 15px;
  border-radius: 8px;
  transition: all 0.3s;
  border-left: 3px solid transparent;
}

.news-item:hover {
  background: #353535;
  border-left-color: #4CAF50;
  transform: translateX(5px);
}

.news-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.news-source {
  font-size: 12px;
  color: #4CAF50;
  font-weight: bold;
}

.news-date {
  font-size: 11px;
  color: #888;
}

.news-title {
  color: #fff;
  text-decoration: none;
  font-size: 15px;
  line-height: 1.5;
  display: block;
}

.news-title:hover {
  color: #4CAF50;
  text-decoration: underline;
}
</style>
