<template>
  <div class="stock-dashboard">
    <header class="dashboard-header">
      <h1>🏦 주식 대시보드</h1>
      
      <div class="user-section">
        <span class="welcome">{{ user?.username }}님 환영합니다!</span>
        <button @click="handleLogout" class="logout-btn">로그아웃</button>
      </div>
    </header>
    
    <StockSearch @search="handleSearch" />

    <!-- 포트폴리오 추가 -->
    <PortfolioPanel ref="portfolioRef" />

    <!-- 관심 종목 패널 -->
    <WatchlistPanel 
      ref="watchlistRef"
      @select="handleWatchlistSelect"
    />
    
    <!-- StockInfo에 이벤트 리스너 추가 -->
    <StockInfo 
      v-if="currentStock"
      :stockData="currentStock"
      :stockCode="searchedCode"
      :stockName="stockName"
      @watchlist-updated="handleWatchlistUpdate"
    />

    <StockChart 
      v-if="currentStock"
      ref="chartRef"
      :stockCode="searchedCode"
      :stockName="stockName"
      @periodChange="handlePeriodChange"
    />

    <StockNews 
      v-if="currentStock"
      :stockCode="searchedCode"
      :stockName="stockName"
    />
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
import WatchlistPanel from '../components/WatchlistPanel.vue'
import PortfolioPanel from '../components/PortfolioPanel.vue'
import { useAuth } from '../stores/auth'

const API_BASE = 'http://localhost:8000/api'

const router = useRouter()
const { user, logout, fetchUser } = useAuth()

const currentStock = ref(null)
const searchedCode = ref('')
const stockName = ref('')
const chartRef = ref(null)
const watchlistRef = ref(null)
const portfolioRef = ref(null) 

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

const handleWatchlistSelect = (code, name) => {
  handleSearch(code, name)
}

// 관심 종목 업데이트 핸들러 (새로 추가)
const handleWatchlistUpdate = () => {
  // WatchlistPanel을 새로고침
  if (watchlistRef.value) {
    watchlistRef.value.fetchWatchlist()
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
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding: 20px 30px;
  background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
  border: 1px solid #333;
}

h1 {
  color: #4CAF50;
  margin: 0;
  font-size: 28px;
  text-shadow: 0 2px 10px rgba(76, 175, 80, 0.3);
}

.user-section {
  display: flex;
  align-items: center;
  gap: 20px;
}

.welcome {
  color: #fff;
  font-size: 16px;
  font-weight: 600;
  padding: 10px 20px;
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.2) 0%, rgba(76, 175, 80, 0.1) 100%);
  border-radius: 10px;
  border: 1px solid rgba(76, 175, 80, 0.3);
}

.logout-btn {
  padding: 10px 24px;
  background: linear-gradient(135deg, #f44336 0%, #da190b 100%);
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
  transition: all 0.3s;
  box-shadow: 0 4px 15px rgba(244, 67, 54, 0.3);
}

.logout-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(244, 67, 54, 0.5);
  background: linear-gradient(135deg, #ff5449 0%, #e91e0f 100%);
}

.logout-btn:active {
  transform: translateY(0);
}
</style>
