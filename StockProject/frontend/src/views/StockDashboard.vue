<template>
  <div class="stock-dashboard">
    <!-- 헤더 -->
    <header class="dashboard-header">
      <div class="header-content">
        <h1>🏦 주식 대시보드</h1>
        <!-- ref 추가! -->
        <StockSearch 
          @search="handleSearch" 
          class="header-search"
          ref="stockSearchRef"
        />
      </div>
      
      <div class="user-section">
        <span class="welcome">{{ user?.username }}님 환영합니다!</span>
        <button @click="handleLogout" class="logout-btn">로그아웃</button>
      </div>
    </header>
    
    <!-- 메인 컨텐츠 -->
    <div class="main-content">
      <!-- 왼쪽: 코스피 상위 종목 -->
        <aside class="left-sidebar">
          <TopStocks 
            ref="topStocksRef"
            @select="handleStockSelect"
            @watchlist-changed="handleWatchlistUpdate"
          />
        </aside>

      <!-- 오른쪽: 포트폴리오 + 뉴스 -->
      <main class="right-content">
        <section class="portfolio-section">
          <PortfolioPanel ref="portfolioRef" />
        </section>

        <section class="news-section">
          <MarketNews />
        </section>
      </main>
    </div>

    <!-- 선택된 종목 상세 정보 (모달) -->
    <div v-if="currentStock" class="stock-detail-modal" @click.self="closeStockDetail">
      <div class="modal-content">
        <button @click="closeStockDetail" class="close-btn">✕</button>
        
        <StockInfo 
          :stockData="currentStock"
          :stockCode="searchedCode"
          :stockName="stockName"
          @watchlist-updated="handleWatchlistUpdate"
        />

        <StockChart 
          ref="chartRef"
          :stockCode="searchedCode"
          :stockName="stockName"
          @periodChange="handlePeriodChange"
        />

        <StockNews 
          :stockCode="searchedCode"
          :stockName="stockName"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import StockSearch from '../components/StockSearch.vue'
import StockInfo from '../components/StockInfo.vue'
import StockChart from '../components/StockChart.vue'
import StockNews from '../components/StockNews.vue'
import PortfolioPanel from '../components/PortfolioPanel.vue'
import TopStocks from '../components/TopStocks.vue'
import MarketNews from '../components/MarketNews.vue'
import { useAuth } from '../stores/auth'

const API_BASE = 'http://localhost:8000/api'

const router = useRouter()
const { user, logout, fetchUser } = useAuth()

const currentStock = ref(null)
const searchedCode = ref('')
const stockName = ref('')
const chartRef = ref(null)
const portfolioRef = ref(null)
const topStocksRef = ref(null)
const stockSearchRef = ref(null)  // ← 추가!

onMounted(async () => {
  await fetchUser()
})

const handleLogout = () => {
  if (confirm('로그아웃 하시겠습니까?')) {
    logout()
    router.push('/login')
  }
}

const handleSearch = async (code, name) => {
  searchedCode.value = code
  stockName.value = name
  
  try {
    const response = await axios.get(`${API_BASE}/stock/current/${code}`)
    if (response.data.rt_cd === '0') {
      currentStock.value = response.data.output
      loadChart(code, 'D')
    } else {
      alert('종목 정보를 가져올 수 없습니다.')
    }
  } catch (error) {
    console.error('주식 정보 조회 실패:', error)
    alert('주식 정보를 가져오는데 실패했습니다.')
  }
}

const handleStockSelect = (code, name) => {
  handleSearch(code, name)
}

const closeStockDetail = () => {
  currentStock.value = null
}

// 관심 종목 업데이트 핸들러 (수정!)
const handleWatchlistUpdate = () => {
  console.log('🔄 관심 종목 업데이트 시작')
  
  // 1. TopStocks 갱신
  if (topStocksRef.value) {
    topStocksRef.value.fetchWatchlist()
    console.log('✅ TopStocks 갱신 완료')
  }
  
  // 2. StockSearch 갱신 (추가!)
  if (stockSearchRef.value) {
    stockSearchRef.value.fetchWatchlist()
    console.log('✅ StockSearch 갱신 완료')
  }
}

const loadChart = async (code, period) => {
  try {
    const response = await axios.get(`${API_BASE}/stock/chart/${code}?period=${period}`)
    if (response.data.rt_cd === '0') {
      const output = response.data.output2.reverse()
      const chartData = {
        labels: output.map(d => d.stck_bsop_date),
        prices: output.map(d => parseInt(d.stck_clpr))
      }
      chartRef.value?.drawChart(chartData)
    }
  } catch (error) {
    console.error('차트 조회 실패:', error)
  }
}

const handlePeriodChange = (period) => {
  loadChart(searchedCode.value, period)
}
</script>

<style scoped>
.stock-dashboard {
  min-height: 100vh;
  background: #121212;
  padding: 20px;
}

/* 헤더 */
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding: 15px 25px;
  background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
  border: 1px solid #333;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 25px;
  flex: 1;
  max-width: none;  /* 제한 제거! */
}

h1 {
  color: #4CAF50;
  margin: 0;
  font-size: 22px;
  text-shadow: 0 2px 10px rgba(76, 175, 80, 0.3);
  white-space: nowrap;
  min-width: 180px;  /* 최소 너비 설정 */
}

/* 검색 영역 - 화면 크기에 따라 확장 */
.header-search {
  flex: 1;  /* 남은 공간 모두 사용 */
  max-width: none;  /* 600px 제한 제거! */
  min-width: 400px;  /* 최소 너비 설정 */
}

.user-section {
  display: flex;
  align-items: center;
  gap: 20px;
  min-width: 250px;  /* 최소 너비 설정 */
}

.welcome {
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  padding: 8px 16px;
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.2) 0%, rgba(76, 175, 80, 0.1) 100%);
  border-radius: 10px;
  border: 1px solid rgba(76, 175, 80, 0.3);
  white-space: nowrap;
}

.logout-btn {
  padding: 8px 20px;
  background: linear-gradient(135deg, #f44336 0%, #da190b 100%);
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 13px;
  font-weight: bold;
  transition: all 0.3s;
  box-shadow: 0 4px 15px rgba(244, 67, 54, 0.3);
}

.logout-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(244, 67, 54, 0.5);
}

/* 메인 컨텐츠 */
.main-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  height: calc(100vh - 120px);
}

.left-sidebar {
  overflow-y: auto;
}

.right-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
  overflow-y: auto;
}

.portfolio-section {
  flex-shrink: 0;
}

.news-section {
  flex: 1;
  min-height: 400px;
}

/* 종목 상세 모달 */
.stock-detail-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
  overflow-y: auto;
}

.modal-content {
  background: #1e1e1e;
  border-radius: 15px;
  padding: 30px;
  max-width: 1200px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  border: 2px solid #444;
}

.close-btn {
  position: absolute;
  top: 20px;
  right: 20px;
  background: #f44336;
  color: white;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  font-size: 24px;
  cursor: pointer;
  transition: all 0.3s;
  z-index: 10;
}

.close-btn:hover {
  background: #da190b;
  transform: rotate(90deg);
}

/* 반응형 - 화면 크기별 최적화 */
@media (min-width: 1920px) {
  /* 큰 화면 (FHD 이상) */
  .header-search {
    max-width: 1200px;  /* 큰 화면에서는 최대 1200px */
  }
}

@media (min-width: 1600px) and (max-width: 1919px) {
  /* 중간-큰 화면 */
  .header-search {
    max-width: 1000px;  /* 최대 1000px */
  }
}

@media (min-width: 1400px) and (max-width: 1599px) {
  /* 중간 화면 */
  .header-search {
    max-width: 800px;  /* 최대 800px */
  }
  
  .main-content {
    grid-template-columns: 2.5fr 1fr;
  }
}

@media (min-width: 1200px) and (max-width: 1399px) {
  /* 작은-중간 화면 */
  .header-search {
    max-width: 700px;
  }
  
  .main-content {
    grid-template-columns: 2fr 1fr;
  }
}

@media (max-width: 1199px) {
  .header-search {
    max-width: 600px;
  }
  
  .main-content {
    grid-template-columns: 1.5fr 1fr;
  }
}

@media (max-width: 1024px) {
  .header-search {
    min-width: 300px;
  }
  
  .main-content {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 15px;
  }
  
  h1 {
    font-size: 20px;
  }
  
  .header-search {
    width: 100%;
    min-width: auto;
  }
  
  .user-section {
    width: 100%;
    justify-content: space-between;
    min-width: auto;
  }
  
  .main-content {
    grid-template-columns: 1fr;
    height: auto;
  }
  
  .left-sidebar {
    max-height: 500px;
  }
}

/* 스크롤바 스타일 */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #1e1e1e;
}

::-webkit-scrollbar-thumb {
  background: #4CAF50;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #45a049;
}
</style>
