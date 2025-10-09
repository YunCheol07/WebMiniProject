<template>
  <div class="portfolio-panel">
    <div class="portfolio-header">
      <h3>💼 내 주식 현황</h3>
      <button @click="showAddModal = true" class="add-btn">+ 종목 추가</button>
    </div>

    <div v-if="!isAuthenticated" class="login-required">
      <p>로그인 후 이용 가능합니다</p>
    </div>

    <div v-else-if="loading" class="loading">
      <p>로딩 중...</p>
    </div>

    <div v-else-if="portfolio.length === 0" class="empty-state">
      <p>보유 종목이 없습니다</p>
      <p class="help-text">+ 종목 추가 버튼을 눌러 보유 주식을 등록하세요</p>
    </div>

    <div v-else class="portfolio-container">
      <!-- 요약 정보 -->
      <div class="summary-card">
        <div class="summary-item">
          <span class="summary-label">총 매입금액</span>
          <span class="summary-value">{{ formatNumber(summary.total_purchase_amount) }}원</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">총 평가금액</span>
          <span class="summary-value primary">{{ formatNumber(summary.total_current_value) }}원</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">평가손익</span>
          <span class="summary-value" :class="profitClass">
            {{ summary.total_profit_loss >= 0 ? '+' : '' }}{{ formatNumber(summary.total_profit_loss) }}원
            ({{ summary.total_profit_loss_rate >= 0 ? '+' : '' }}{{ summary.total_profit_loss_rate }}%)
          </span>
        </div>
      </div>

      <!-- 보유 종목 테이블 -->
      <div class="portfolio-table">
        <table>
          <thead>
            <tr>
              <th>종목명</th>
              <th>보유수량</th>
              <th>평균매입가</th>
              <th>현재가</th>
              <th>평가금액</th>
              <th>손익</th>
              <th>수익률</th>
              <th>삭제</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in portfolio" :key="item.portfolio_id">
              <td class="stock-name">{{ item.stock_name }}</td>
              <td>{{ formatNumber(item.quantity) }}주</td>
              <td>{{ formatNumber(item.avg_price) }}원</td>
              <td>{{ formatNumber(item.current_price) }}원</td>
              <td>{{ formatNumber(item.current_value) }}원</td>
              <td :class="item.profit_loss >= 0 ? 'profit' : 'loss'">
                {{ item.profit_loss >= 0 ? '+' : '' }}{{ formatNumber(item.profit_loss) }}원
              </td>
              <td :class="item.profit_loss_rate >= 0 ? 'profit' : 'loss'">
                {{ item.profit_loss_rate >= 0 ? '+' : '' }}{{ item.profit_loss_rate }}%
              </td>
              <td>
                <button @click="removeItem(item)" class="delete-btn">✕</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 종목 추가 모달 -->
    <div v-if="showAddModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <h3>보유 종목 추가</h3>
        
        <form @submit.prevent="addPortfolio">
          <!-- 종목 검색 (자동완성) -->
          <div class="form-group">
            <label>종목 검색</label>
            <div class="search-wrapper">
              <input 
                v-model="stockSearchQuery" 
                @input="handleStockSearch"
                @focus="showSearchResults = true"
                type="text" 
                placeholder="종목명 또는 종목코드 입력 (예: 삼성전자, 005930)"
                autocomplete="off"
              />
              
              <!-- 자동완성 결과 -->
              <div v-if="showSearchResults && stockSearchResults.length > 0" class="search-results">
                <div 
                  v-for="stock in stockSearchResults" 
                  :key="stock.stock_code"
                  class="search-result-item"
                  @click="selectStock(stock)"
                >
                  <span class="result-name">{{ stock.stock_name }}</span>
                  <span class="result-code">{{ stock.stock_code }}</span>
                </div>
              </div>

              <div v-if="showSearchResults && stockSearchQuery && stockSearchResults.length === 0" class="no-results">
                검색 결과가 없습니다
              </div>
            </div>
          </div>

          <!-- 선택된 종목 표시 -->
          <div v-if="selectedStock" class="selected-stock">
            <span class="selected-label">선택된 종목:</span>
            <span class="selected-name">{{ selectedStock.stock_name }} ({{ selectedStock.stock_code }})</span>
          </div>

          <div class="form-group">
            <label>보유 수량</label>
            <input 
              v-model.number="formData.quantity" 
              type="number" 
              placeholder="예: 10"
              min="1"
              required
            />
          </div>

          <div class="form-group">
            <label>평균 매입가</label>
            <input 
              v-model.number="formData.avg_price" 
              type="number" 
              placeholder="예: 70000"
              min="1"
              required
            />
          </div>

          <div class="form-group">
            <label>매입 날짜</label>
            <input 
              v-model="formData.purchase_date" 
              type="date" 
              required
            />
          </div>

          <div v-if="error" class="error-message">{{ error }}</div>

          <div class="modal-buttons">
            <button type="button" @click="closeModal" class="cancel-btn">취소</button>
            <button type="submit" class="submit-btn" :disabled="!selectedStock">추가</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useAuth } from '../stores/auth'

const API_BASE = 'http://localhost:8000/api'

const { isAuthenticated } = useAuth()

const portfolio = ref([])
const summary = ref({
  total_purchase_amount: 0,
  total_current_value: 0,
  total_profit_loss: 0,
  total_profit_loss_rate: 0
})
const loading = ref(false)
const showAddModal = ref(false)
const error = ref('')

// 종목 검색 관련
const stockSearchQuery = ref('')
const stockSearchResults = ref([])
const showSearchResults = ref(false)
const selectedStock = ref(null)
let searchTimeout = null

const formData = ref({
  stock_code: '',
  quantity: 1,
  avg_price: 0,
  purchase_date: new Date().toISOString().split('T')[0]
})

const profitClass = computed(() => {
  return summary.value.total_profit_loss >= 0 ? 'profit' : 'loss'
})

const formatNumber = (value) => {
  if (!value) return '0'
  return parseInt(value).toLocaleString()
}

// 종목 검색 (자동완성)
const handleStockSearch = async () => {
  const query = stockSearchQuery.value.trim()
  
  if (!query) {
    stockSearchResults.value = []
    return
  }
  
  clearTimeout(searchTimeout)
  
  searchTimeout = setTimeout(async () => {
    try {
      const response = await axios.get(`${API_BASE}/stocks/search`, {
        params: { q: query, limit: 10 }
      })
      
      if (response.data.success) {
        stockSearchResults.value = response.data.stocks
        showSearchResults.value = true
      }
    } catch (error) {
      console.error('종목 검색 실패:', error)
      stockSearchResults.value = []
    }
  }, 300)
}

// 종목 선택
const selectStock = (stock) => {
  selectedStock.value = stock
  stockSearchQuery.value = `${stock.stock_name} (${stock.stock_code})`
  formData.value.stock_code = stock.stock_code
  showSearchResults.value = false
}

// 모달 닫기
const closeModal = () => {
  showAddModal.value = false
  stockSearchQuery.value = ''
  stockSearchResults.value = []
  selectedStock.value = null
  error.value = ''
  formData.value = {
    stock_code: '',
    quantity: 1,
    avg_price: 0,
    purchase_date: new Date().toISOString().split('T')[0]
  }
}

const fetchPortfolio = async () => {
  const token = localStorage.getItem('token')
  if (!token) return

  loading.value = true

  try {
    const response = await axios.get(`${API_BASE}/portfolio`, {
      headers: { Authorization: `Bearer ${token}` }
    })

    if (response.data.success) {
      portfolio.value = response.data.portfolio
      summary.value = response.data.summary
    }
  } catch (error) {
    console.error('포트폴리오 조회 실패:', error)
  } finally {
    loading.value = false
  }
}

const addPortfolio = async () => {
  if (!selectedStock.value) {
    error.value = '종목을 선택해주세요'
    return
  }

  const token = localStorage.getItem('token')
  error.value = ''

  try {
    const response = await axios.post(
      `${API_BASE}/portfolio`,
      formData.value,
      {
        headers: { Authorization: `Bearer ${token}` }
      }
    )

    if (response.data.success) {
      alert(response.data.message)
      closeModal()
      fetchPortfolio()
    }
  } catch (err) {
    error.value = err.response?.data?.detail || '추가에 실패했습니다'
  }
}

const removeItem = async (item) => {
  if (!confirm(`${item.stock_name}을(를) 포트폴리오에서 삭제하시겠습니까?`)) {
    return
  }

  const token = localStorage.getItem('token')

  try {
    const response = await axios.delete(
      `${API_BASE}/portfolio/${item.portfolio_id}`,
      {
        headers: { Authorization: `Bearer ${token}` }
      }
    )

    if (response.data.success) {
      fetchPortfolio()
    }
  } catch (error) {
    console.error('포트폴리오 삭제 실패:', error)
    alert('삭제에 실패했습니다')
  }
}

// 외부 클릭 시 검색 결과 숨기기
document.addEventListener('click', (e) => {
  if (!e.target.closest('.search-wrapper')) {
    showSearchResults.value = false
  }
})

onMounted(() => {
  if (isAuthenticated.value) {
    fetchPortfolio()
  }
})

defineExpose({ fetchPortfolio })
</script>

<style scoped>
.portfolio-panel {
  background: #1e1e1e;
  padding: 20px;
  border-radius: 10px;
  margin-top: 20px;
}

.portfolio-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

/* 제목 크기 감소 */
h3 {
  color: #4CAF50;
  font-size: 18px;  /* ← 20px에서 18px로 감소 */
  margin: 0;
}

.add-btn {
  padding: 8px 16px;  /* ← 10px 20px에서 감소 */
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;  /* ← 14px에서 13px로 감소 */
  font-weight: bold;
  transition: all 0.3s;
}

.add-btn:hover {
  background: #45a049;
  transform: translateY(-2px);
}

.login-required,
.loading,
.empty-state {
  text-align: center;
  padding: 40px;
  color: #888;
}

.help-text {
  font-size: 13px;  /* ← 14px에서 13px로 감소 */
  color: #666;
  margin-top: 10px;
}

.summary-card {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
  margin-bottom: 30px;
}

.summary-item {
  background: #2d2d2d;
  padding: 16px;  /* ← 20px에서 16px로 감소 */
  border-radius: 10px;
  border: 2px solid #444;
}

/* 요약 라벨 크기 감소 */
.summary-label {
  display: block;
  color: #aaa;
  font-size: 12px;  /* ← 14px에서 12px로 감소 */
  margin-bottom: 8px;
}

/* 요약 값 크기 감소 */
.summary-value {
  display: block;
  color: white;
  font-size: 20px;  /* ← 24px에서 20px로 감소 */
  font-weight: bold;
}

.summary-value.primary {
  color: #4CAF50;
}

.summary-value.profit {
  color: #f44336;
}

.summary-value.loss {
  color: #2196F3;
}

.portfolio-table {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: #2d2d2d;
}

/* 테이블 헤더 크기 감소 */
th {
  padding: 12px;  /* ← 15px에서 12px로 감소 */
  text-align: left;
  color: #aaa;
  font-size: 13px;  /* ← 14px에서 13px로 감소 */
  font-weight: 600;
  border-bottom: 2px solid #444;
}

/* 테이블 데이터 크기 감소 */
td {
  padding: 12px;  /* ← 15px에서 12px로 감소 */
  color: white;
  font-size: 14px;  /* ← 추가: 명시적으로 14px 설정 */
  border-bottom: 1px solid #333;
}

.stock-name {
  font-weight: 600;
  color: #4CAF50;
  font-size: 14px;  /* ← 추가: 명시적 설정 */
}

.profit {
  color: #f44336;
  font-weight: bold;
}

.loss {
  color: #2196F3;
  font-weight: bold;
}

.delete-btn {
  background: #f44336;
  color: white;
  border: none;
  border-radius: 50%;
  width: 28px;  /* ← 30px에서 28px로 감소 */
  height: 28px;  /* ← 30px에서 28px로 감소 */
  cursor: pointer;
  font-size: 16px;  /* ← 추가: X 버튼 크기 */
  transition: all 0.3s;
}

.delete-btn:hover {
  background: #da190b;
  transform: scale(1.1);
}

/* 모달 스타일 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: #1e1e1e;
  padding: 30px;
  border-radius: 15px;
  width: 90%;
  max-width: 500px;
  border: 2px solid #444;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-content h3 {
  margin-bottom: 20px;
  font-size: 18px;  /* ← 모달 제목 크기도 통일 */
}

.form-group {
  margin-bottom: 20px;
}

/* 라벨 크기 감소 */
label {
  display: block;
  color: #aaa;
  font-size: 13px;  /* ← 14px에서 13px로 감소 */
  margin-bottom: 8px;
}

/* 인풋 크기 감소 */
input {
  width: 100%;
  padding: 10px;  /* ← 12px에서 10px로 감소 */
  background: #2d2d2d;
  border: 2px solid #444;
  border-radius: 8px;
  color: white;
  font-size: 14px;  /* ← 16px에서 14px로 감소 */
}

input:focus {
  outline: none;
  border-color: #4CAF50;
}

/* 종목 검색 자동완성 */
.search-wrapper {
  position: relative;
}

.search-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: #2d2d2d;
  border: 2px solid #444;
  border-radius: 8px;
  margin-top: 5px;
  max-height: 250px;
  overflow-y: auto;
  z-index: 1001;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
}

.search-result-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 14px;  /* ← 12px 16px에서 감소 */
  cursor: pointer;
  transition: background 0.2s;
  border-bottom: 1px solid #333;
}

.search-result-item:last-child {
  border-bottom: none;
}

.search-result-item:hover {
  background: #353535;
}

/* 검색 결과 텍스트 크기 감소 */
.result-name {
  color: white;
  font-weight: 600;
  font-size: 14px;  /* ← 15px에서 14px로 감소 */
}

.result-code {
  color: #888;
  font-size: 12px;  /* ← 13px에서 12px로 감소 */
}

.no-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: #2d2d2d;
  border: 2px solid #444;
  border-radius: 8px;
  margin-top: 5px;
  padding: 16px;
  text-align: center;
  color: #888;
  font-size: 13px;  /* ← 추가 */
  z-index: 1001;
}

.selected-stock {
  padding: 10px;  /* ← 12px에서 10px로 감소 */
  background: rgba(76, 175, 80, 0.1);
  border: 2px solid #4CAF50;
  border-radius: 8px;
  margin-bottom: 20px;
}

.selected-label {
  color: #aaa;
  font-size: 13px;  /* ← 14px에서 13px로 감소 */
  margin-right: 10px;
}

.selected-name {
  color: #4CAF50;
  font-weight: 600;
  font-size: 14px;  /* ← 16px에서 14px로 감소 */
}

.error-message {
  background: rgba(244, 67, 54, 0.1);
  border: 1px solid #f44336;
  color: #f44336;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 20px;
  text-align: center;
  font-size: 13px;  /* ← 추가 */
}

.modal-buttons {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

/* 버튼 크기 감소 */
.cancel-btn,
.submit-btn {
  padding: 10px 20px;  /* ← 12px 24px에서 감소 */
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;  /* ← 16px에서 14px로 감소 */
  font-weight: bold;
  transition: all 0.3s;
}

.cancel-btn {
  background: #555;
  color: white;
}

.cancel-btn:hover {
  background: #666;
}

.submit-btn {
  background: #4CAF50;
  color: white;
}

.submit-btn:hover:not(:disabled) {
  background: #45a049;
}

.submit-btn:disabled {
  background: #555;
  cursor: not-allowed;
  opacity: 0.5;
}
</style>
