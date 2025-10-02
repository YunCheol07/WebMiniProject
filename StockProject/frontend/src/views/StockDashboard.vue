<template>
  <div class="stock-dashboard">
    <!-- 헤더 -->
    <header class="dashboard-header">
      <h1>🏦 주식 대시보드</h1>
      
      <div class="user-section">
        <span class="welcome">{{ user?.username }}님 환영합니다!</span>
        <button @click="handleLogout" class="logout-btn">로그아웃</button>
      </div>
    </header>
    
    <StockSearch @search="handleSearch" />
    
    <StockInfo 
      v-if="currentStock"
      :stockData="currentStock"
      :stockCode="searchedCode"
      :stockName="stockName"
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
import { useAuth } from '../stores/auth'

const API_BASE = 'http://localhost:8000/api'

const router = useRouter()
const { user, logout, fetchUser } = useAuth()

const currentStock = ref(null)
const searchedCode = ref('')
const stockName = ref('')
const chartRef = ref(null)

const stockNames = {
  '005930': '삼성전자',
  '000660': 'SK하이닉스',
  '035420': 'NAVER',
  '035720': '카카오',
  '005380': '현대차',
  '051910': 'LG화학',
  '006400': '삼성SDI',
  '000270': '기아',
  '207940': '삼성바이오로직스',
  '068270': '셀트리온',
  '005490': 'POSCO홀딩스',
  '105560': 'KB금융',
  '055550': '신한지주',
  '012330': '현대모비스',
  '028260': '삼성물산'
}

onMounted(async () => {
  await fetchUser()
})

const handleLogout = () => {
  if (confirm('로그아웃 하시겠습니까?')) {
    logout()
    router.push('/login')
  }
}

const handleSearch = async (code) => {
  searchedCode.value = code
  stockName.value = stockNames[code] || `종목 ${code}`
  
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
  padding: 20px;
  background: #1e1e1e;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

h1 {
  color: #4CAF50;
  margin: 0;
  font-size: 28px;
}

.user-section {
  display: flex;
  align-items: center;
  gap: 20px;
}

.welcome {
  color: #aaa;
  font-size: 16px;
  font-weight: 500;
}

.logout-btn {
  padding: 10px 20px;
  background: linear-gradient(135deg, #f44336 0%, #da190b 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
  transition: all 0.3s;
  box-shadow: 0 2px 10px rgba(244, 67, 54, 0.3);
}

.logout-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(244, 67, 54, 0.4);
}
</style>
