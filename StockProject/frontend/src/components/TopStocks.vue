<template>
  <div class="top-stocks">
    <!-- 고정 영역: 제목 + 테이블 헤더 -->
    <div class="fixed-header-section">
      <h3>📊 코스피 시가총액 TOP 20</h3>  <!-- ← TOP 30에서 20으로 변경 -->
      
      <div v-if="loading" class="loading">
        <p>로딩 중...</p>
      </div>

      <div v-else class="table-header">
        <div class="header-rank"></div>
        <div class="header-item">종목명</div>
        <div class="header-item">현재가</div>
        <div class="header-item">등락률</div>
        <div class="header-item">거래량</div>
        <div class="header-item">시가총액</div>
      </div>
    </div>

    <!-- 스크롤 영역: 종목 리스트만 -->
    <div v-if="!loading" class="stocks-list-container">
      <div class="stocks-list">
        <div 
          v-for="stock in stocks" 
          :key="stock.stock_code"
          class="stock-item"
          @click="selectStock(stock)"
        >
          <!-- 순위 + 하트 (가로) -->
          <div class="rank-heart-section">
            <button 
              @click.stop="toggleWatchlist(stock)"
              class="heart-btn"
              :class="{ active: isInWatchlist(stock.stock_code) }"
            >
              {{ isInWatchlist(stock.stock_code) ? '❤️' : '🤍' }}
            </button>
            <span class="rank">{{ stock.rank }}</span>
          </div>

          <!-- 종목명 (코드 제거) -->
          <div class="info-column name-column">
            <div class="stock-name">{{ stock.stock_name }}</div>
            <!-- ↓ 종목 코드 줄 삭제됨 -->
          </div>

          <!-- 현재가 -->
          <div class="info-column">
            <div class="value price">{{ formatNumber(stock.current_price) }}원</div>
          </div>

          <!-- 등락률 -->
          <div class="info-column">
            <div class="value" :class="stock.change_rate >= 0 ? 'positive' : 'negative'">
              {{ stock.change_rate >= 0 ? '+' : '' }}{{ stock.change_rate }}%
            </div>
          </div>

          <!-- 거래량 -->
          <div class="info-column">
            <div class="value">{{ formatVolume(stock.volume) }}</div>
          </div>

          <!-- 시가총액 -->
          <div class="info-column">
            <div class="value market-cap">{{ stock.market_cap_formatted }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, defineEmits } from 'vue'
import axios from 'axios'

const emit = defineEmits(['select', 'watchlist-changed'])

const API_BASE = 'http://localhost:8000/api'

const stocks = ref([])
const loading = ref(false)
const watchlistCodes = ref(new Set())

const formatNumber = (value) => {
  return parseInt(value).toLocaleString()
}

const formatVolume = (value) => {
  const vol = parseInt(value)
  if (vol >= 1000000) {
    return (vol / 1000000).toFixed(1) + 'M'
  } else if (vol >= 1000) {
    return (vol / 1000).toFixed(1) + 'K'
  }
  return vol.toLocaleString()
}

const isInWatchlist = (stockCode) => {
  return watchlistCodes.value.has(stockCode)
}

const fetchTopStocks = async () => {
  loading.value = true

  try {
    const response = await axios.get(`${API_BASE}/stock/top-stocks`, {
      params: { limit: 20 }  // ← 30에서 20으로 변경
    })

    if (response.data.success) {
      stocks.value = response.data.stocks
    }
  } catch (error) {
    console.error('상위 종목 조회 실패:', error)
  } finally {
    loading.value = false
  }
}

const fetchWatchlist = async () => {
  const token = localStorage.getItem('token')
  if (!token) return

  try {
    const response = await axios.get(`${API_BASE}/watchlist`, {
      headers: { Authorization: `Bearer ${token}` }
    })

    if (response.data.success) {
      watchlistCodes.value = new Set(
        response.data.watchlist.map(item => item.stock_code)
      )
    }
  } catch (error) {
    console.error('관심 종목 조회 실패:', error)
  }
}

const toggleWatchlist = async (stock) => {
  const token = localStorage.getItem('token')
  if (!token) {
    alert('로그인이 필요합니다')
    return
  }

  try {
    if (isInWatchlist(stock.stock_code)) {
      await axios.delete(`${API_BASE}/watchlist/${stock.stock_code}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      watchlistCodes.value.delete(stock.stock_code)
    } else {
      await axios.post(
        `${API_BASE}/watchlist/${stock.stock_code}`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      )
      watchlistCodes.value.add(stock.stock_code)
    }
    
    emit('watchlist-changed')
    
  } catch (error) {
    console.error('관심 종목 토글 실패:', error)
  }
}

const selectStock = (stock) => {
  emit('select', stock.stock_code, stock.stock_name)
}

onMounted(() => {
  fetchTopStocks()
  fetchWatchlist()
})

defineExpose({ fetchTopStocks, fetchWatchlist })
</script>

<style scoped>
.top-stocks {
  background: #1e1e1e;
  border-radius: 10px;
  padding: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.fixed-header-section {
  flex-shrink: 0;
  background: #1e1e1e;
  padding-bottom: 10px;
}

/* 제목 - 글자 크기 증가 */
h3 {
  color: #4CAF50;
  font-size: 24px;
  font-weight: 700;
  margin: 0 0 15px 0;
  padding: 0;
  border-bottom: 2px solid #333;
  padding-bottom: 12px;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #888;
}

.table-header {
  display: grid;
  grid-template-columns: 80px 1.5fr 1fr 0.8fr 0.8fr 1fr;
  gap: 12px;
  padding: 12px 15px;
  background: #2d2d2d;
  border-radius: 8px;
  border: 2px solid #444;
}

.header-rank {
  /* 순위 + 하트 자리 */
}

/* 테이블 헤더 컬럼명 크기 증가 */
.header-item {
  font-size: 16px;  /* ← 13px에서 16px로 증가 */
  font-weight: 600;
  color: #aaa;
  text-align: left;
}

.stocks-list-container {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  margin-top: 10px;
  padding-right: 5px;
}

.stocks-list-container::-webkit-scrollbar {
  width: 8px;
}

.stocks-list-container::-webkit-scrollbar-track {
  background: #1e1e1e;
  border-radius: 10px;
}

.stocks-list-container::-webkit-scrollbar-thumb {
  background: #4CAF50;
  border-radius: 10px;
}

.stocks-list-container::-webkit-scrollbar-thumb:hover {
  background: #45a049;
}

.stocks-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stock-item {
  background: #2d2d2d;
  border: 2px solid #444;
  border-radius: 8px;
  padding: 12px 15px;
  cursor: pointer;
  transition: all 0.3s;
  display: grid;
  grid-template-columns: 80px 1.5fr 1fr 0.8fr 0.8fr 1fr;
  gap: 12px;
  align-items: center;
}

.stock-item:hover {
  border-color: #4CAF50;
  background: #353535;
  transform: translateX(3px);
}

.rank-heart-section {
  display: flex;
  align-items: center;
  gap: 8px;
}

.heart-btn {
  background: none;
  border: none;
  font-size: 20px;  /* ← 18px에서 20px로 증가 */
  cursor: pointer;
  transition: transform 0.2s;
  padding: 0;
}

.heart-btn:hover {
  transform: scale(1.2);
}

/* 순위 크기 증가 */
.rank {
  font-size: 18px;  /* ← 16px에서 18px로 증가 */
  font-weight: bold;
  color: #4CAF50;
  min-width: 25px;
}

.info-column {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.name-column {
  gap: 3px;
}

/* 값 크기 증가 */
.value {
  font-size: 16px;  /* ← 14px에서 16px로 증가 */
  font-weight: 600;
  color: white;
}

/* 현재가 크기 증가 */
.value.price {
  font-size: 17px;  /* ← 15px에서 17px로 증가 */
  color: #fff;
}

.value.positive {
  color: #f44336;
}

.value.negative {
  color: #2196F3;
}

/* 시가총액 크기 증가 */
.value.market-cap {
  color: #4CAF50;
  font-size: 15px;  /* ← 13px에서 15px로 증가 */
}

/* 종목명 크기 증가 */
.stock-name {
  font-size: 17px;  /* ← 15px에서 17px로 증가 */
  font-weight: 600;
  color: white;
}
</style>
