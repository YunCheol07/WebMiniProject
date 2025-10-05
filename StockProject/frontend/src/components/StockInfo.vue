<template>
  <div class="stock-info">
    <div class="stock-header">
      <div class="stock-title">
        <h2>📊 {{ stockName }} ({{ stockCode }})</h2>
        <span class="market-status">업종: {{ stockData.bstp_kor_isnm || '운송장비·부품' }}</span>
      </div>
      
      <!-- 하트 버튼 추가 -->
      <button 
        @click="toggleWatchlist" 
        class="watchlist-btn"
        :class="{ active: isInWatchlist }"
        :disabled="loading"
      >
        <span class="heart-icon">{{ isInWatchlist ? '❤️' : '🤍' }}</span>
        <span class="btn-text">{{ isInWatchlist ? '관심 종목' : '관심 등록' }}</span>
      </button>
    </div>

    <div class="stock-grid">
      <!-- 현재가 -->
      <div class="info-card">
        <div class="card-label">현재가</div>
        <div class="card-value primary">{{ formatNumber(stockData.stck_prpr) }}원</div>
      </div>

      <!-- 전일대비 -->
      <div class="info-card">
        <div class="card-label">전일대비</div>
        <div class="card-value" :class="priceChangeClass">
          {{ priceChangeSign }}{{ formatNumber(stockData.prdy_vrss) }}원 ({{ priceChangeSign }}{{ stockData.prdy_ctrt }}%)
        </div>
      </div>

      <!-- 시가 -->
      <div class="info-card">
        <div class="card-label">시가</div>
        <div class="card-value">{{ formatNumber(stockData.stck_oprc) }}원</div>
      </div>

      <!-- 거래량 -->
      <div class="info-card">
        <div class="card-label">거래량</div>
        <div class="card-value">{{ formatNumber(stockData.acml_vol) }}주</div>
      </div>
    </div>

    <!-- 상세 정보 -->
    <div class="detail-section">
      <h3>상세 정보</h3>
      <div class="detail-grid">
        <div class="detail-item">
          <span class="detail-label">고가:</span>
          <span class="detail-value">{{ formatNumber(stockData.stck_hgpr) }}원</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">저가:</span>
          <span class="detail-value">{{ formatNumber(stockData.stck_lwpr) }}원</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">52주 최고가:</span>
          <span class="detail-value">{{ formatNumber(stockData.w52_hgpr) }}원</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">52주 최저가:</span>
          <span class="detail-value">{{ formatNumber(stockData.w52_lwpr) }}원</span>
        </div>
      </div>
    </div>

    <!-- 투자지표 -->
    <div class="indicator-section">
      <h3>투자지표</h3>
      <div class="indicator-grid">
        <div class="indicator-item">
          <span class="indicator-label">PER:</span>
          <span class="indicator-value">{{ stockData.per || '-' }}</span>
        </div>
        <div class="indicator-item">
          <span class="indicator-label">PBR:</span>
          <span class="indicator-value">{{ stockData.pbr || '-' }}</span>
        </div>
        <div class="indicator-item">
          <span class="indicator-label">EPS:</span>
          <span class="indicator-value">{{ formatNumber(stockData.eps) }}원</span>
        </div>
        <div class="indicator-item">
          <span class="indicator-label">BPS:</span>
          <span class="indicator-value">{{ formatNumber(stockData.bps) }}원</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, defineProps, watch } from 'vue'
import axios from 'axios'

const props = defineProps({
  stockData: Object,
  stockCode: String,
  stockName: String
})

const API_BASE = 'http://localhost:8000/api'

const isInWatchlist = ref(false)
const loading = ref(false)

// 가격 변동 표시
const priceChangeClass = computed(() => {
  const change = parseInt(props.stockData.prdy_vrss)
  if (change > 0) return 'positive'
  if (change < 0) return 'negative'
  return 'neutral'
})

const priceChangeSign = computed(() => {
  const change = parseInt(props.stockData.prdy_vrss)
  if (change > 0) return '+'
  if (change < 0) return ''
  return ''
})

// 숫자 포맷팅
const formatNumber = (value) => {
  if (!value) return '0'
  return parseInt(value).toLocaleString()
}

// 관심 종목 상태 확인
const checkWatchlist = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      isInWatchlist.value = false
      return
    }

    const response = await axios.get(
      `${API_BASE}/watchlist/check/${props.stockCode}`,
      {
        headers: { Authorization: `Bearer ${token}` }
      }
    )
    
    isInWatchlist.value = response.data.in_watchlist
  } catch (error) {
    console.error('관심 종목 확인 실패:', error)
    isInWatchlist.value = false
  }
}

// 관심 종목 토글
const toggleWatchlist = async () => {
  const token = localStorage.getItem('token')
  if (!token) {
    alert('로그인이 필요합니다')
    return
  }

  loading.value = true

  try {
    if (isInWatchlist.value) {
      // 삭제
      const response = await axios.delete(
        `${API_BASE}/watchlist/${props.stockCode}`,
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      )
      
      if (response.data.success) {
        isInWatchlist.value = false
        alert('관심 종목에서 삭제되었습니다')
      }
    } else {
      // 추가
      const response = await axios.post(
        `${API_BASE}/watchlist/${props.stockCode}`,
        {},
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      )
      
      if (response.data.success) {
        isInWatchlist.value = true
        alert('관심 종목에 추가되었습니다')
      } else {
        alert(response.data.message)
      }
    }
  } catch (error) {
    console.error('관심 종목 토글 실패:', error)
    alert('오류가 발생했습니다')
  } finally {
    loading.value = false
  }
}

// 종목 변경 시 관심 종목 상태 확인
watch(() => props.stockCode, () => {
  if (props.stockCode) {
    checkWatchlist()
  }
}, { immediate: true })
</script>

<style scoped>
.stock-info {
  background: #1e1e1e;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 20px;
}

.stock-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #333;
}

.stock-title h2 {
  color: #4CAF50;
  margin: 0 0 8px 0;
  font-size: 24px;
}

.market-status {
  color: #888;
  font-size: 14px;
}

/* 하트 버튼 스타일 */
.watchlist-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: #2d2d2d;
  border: 2px solid #444;
  border-radius: 10px;
  color: white;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.3s;
}

.watchlist-btn:hover:not(:disabled) {
  background: #353535;
  border-color: #4CAF50;
  transform: translateY(-2px);
}

.watchlist-btn.active {
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
  border-color: #ff6b6b;
  box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
}

.watchlist-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.heart-icon {
  font-size: 20px;
}

.btn-text {
  font-size: 14px;
}

.stock-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 30px;
}

.info-card {
  background: #2d2d2d;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #444;
}

.card-label {
  color: #888;
  font-size: 14px;
  margin-bottom: 8px;
}

.card-value {
  font-size: 20px;
  font-weight: bold;
  color: white;
}

.card-value.primary {
  color: #4CAF50;
  font-size: 24px;
}

.card-value.positive {
  color: #f44336;
}

.card-value.negative {
  color: #2196F3;
}

.card-value.neutral {
  color: #888;
}

.detail-section,
.indicator-section {
  margin-top: 20px;
}

h3 {
  color: #4CAF50;
  margin-bottom: 15px;
  font-size: 18px;
}

.detail-grid,
.indicator-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
}

.detail-item,
.indicator-item {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  background: #2d2d2d;
  border-radius: 6px;
}

.detail-label,
.indicator-label {
  color: #aaa;
  font-size: 14px;
}

.detail-value,
.indicator-value {
  color: white;
  font-weight: 600;
  font-size: 14px;
}
</style>
