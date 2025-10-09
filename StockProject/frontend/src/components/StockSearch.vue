<template>
  <div class="stock-search-horizontal">
    <div class="search-section">
      <h2>📈 주식 검색</h2>
      
      <div class="search-box">
        <div class="search-wrapper">
          <input 
            v-model="searchQuery" 
            @input="handleSearchInput"
            @keydown.enter="handleEnterKey"
            @keydown.down="highlightNext"
            @keydown.up="highlightPrev"
            @focus="showResults = true"
            placeholder="종목명 또는 종목코드 입력"
            autocomplete="off"
            ref="searchInput"
          />
          <button @click="searchStock" :disabled="!selectedStock" class="search-btn">
            🔍 조회
          </button>

          <!-- 자동완성 결과 -->
          <div v-if="showResults && searchResults.length > 0" class="search-results">
            <div 
              v-for="(stock, index) in searchResults" 
              :key="stock.stock_code"
              :class="['result-item', { highlighted: highlightedIndex === index }]"
              @click="selectStock(stock)"
              @mouseenter="highlightedIndex = index"
            >
              <span class="stock-name">{{ stock.stock_name }}</span>
              <span class="stock-code">{{ stock.stock_code }}</span>
            </div>
          </div>

          <div v-if="showResults && searchQuery && searchResults.length === 0" class="no-results">
            검색 결과가 없습니다
          </div>
        </div>
      </div>

      <!-- 선택된 종목 표시 -->
      <div v-if="selectedStock" class="selected-stock">
        <span class="selected-label">선택:</span>
        <span class="selected-name">{{ selectedStock.stock_name }} ({{ selectedStock.stock_code }})</span>
      </div>
    </div>

    <!-- 관심 종목 섹션 (옆으로) -->
    <div class="watchlist-section">
      <h2>⭐ 관심 종목</h2>
      
      <div v-if="watchlistStocks.length === 0" class="empty-watchlist">
        <p>관심 종목이 없습니다</p>
      </div>
      
      <div v-else class="watchlist-buttons">
        <button 
          v-for="stock in watchlistStocks.slice(0, 5)" 
          :key="stock.stock_code"
          @click="quickSelect(stock.stock_code, stock.stock_name)"
          class="watchlist-btn"
        >
          {{ stock.stock_name }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, defineEmits } from 'vue'
import axios from 'axios'

const emit = defineEmits(['search'])

const API_BASE = 'http://localhost:8000/api'

const searchQuery = ref('')
const searchResults = ref([])
const showResults = ref(false)
const selectedStock = ref(null)
const searchInput = ref(null)
const highlightedIndex = ref(-1)
const watchlistStocks = ref([])

let searchTimeout = null

const handleSearchInput = async () => {
  const query = searchQuery.value.trim()
  
  if (!query) {
    searchResults.value = []
    selectedStock.value = null
    highlightedIndex.value = -1
    return
  }
  
  clearTimeout(searchTimeout)
  
  searchTimeout = setTimeout(async () => {
    try {
      const response = await axios.get(`${API_BASE}/stocks/search`, {
        params: { q: query, limit: 10 }
      })
      
      if (response.data.success) {
        searchResults.value = response.data.stocks
        showResults.value = true
        highlightedIndex.value = -1
      }
    } catch (error) {
      console.error('검색 실패:', error)
      searchResults.value = []
    }
  }, 300)
}

const highlightNext = () => {
  if (searchResults.value.length > 0) {
    highlightedIndex.value = Math.min(
      highlightedIndex.value + 1,
      searchResults.value.length - 1
    )
  }
}

const highlightPrev = () => {
  highlightedIndex.value = Math.max(highlightedIndex.value - 1, -1)
}

const handleEnterKey = () => {
  if (highlightedIndex.value >= 0 && searchResults.value[highlightedIndex.value]) {
    selectStock(searchResults.value[highlightedIndex.value])
    searchStock()
  } 
  else if (searchResults.value.length > 0) {
    selectStock(searchResults.value[0])
    searchStock()
  }
  else if (selectedStock.value) {
    searchStock()
  }
}

const selectStock = (stock) => {
  selectedStock.value = stock
  searchQuery.value = `${stock.stock_name} (${stock.stock_code})`
  showResults.value = false
  highlightedIndex.value = -1
}

const searchStock = () => {
  if (selectedStock.value) {
    emit('search', selectedStock.value.stock_code, selectedStock.value.stock_name)
  }
}

const quickSelect = (code, name) => {
  selectedStock.value = { stock_code: code, stock_name: name }
  searchQuery.value = `${name} (${code})`
  emit('search', code, name)
}

const fetchWatchlist = async () => {
  const token = localStorage.getItem('token')
  if (!token) return

  try {
    const response = await axios.get(`${API_BASE}/watchlist`, {
      headers: { Authorization: `Bearer ${token}` }
    })

    if (response.data.success) {
      watchlistStocks.value = response.data.watchlist
    }
  } catch (error) {
    console.error('관심 종목 조회 실패:', error)
  }
}

onMounted(() => {
  fetchWatchlist()
})

document.addEventListener('click', (e) => {
  if (!e.target.closest('.stock-search-horizontal')) {
    showResults.value = false
  }
})

defineExpose({ fetchWatchlist })
</script>

<style scoped>
/* 가로 배치 */
.stock-search-horizontal {
  display: grid;
  grid-template-columns: 1fr 1fr;  /* 검색 : 관심종목 = 1:1 */
  gap: 20px;
  padding: 15px 20px;
  background: #1e1e1e;
  border-radius: 10px;
  margin-bottom: 15px;
}

h2 {
  color: #4CAF50;
  margin-bottom: 12px;
  font-size: 16px;
  font-weight: 600;
}

/* 검색 섹션 */
.search-section {
  flex: 1;
}

.search-box {
  margin-bottom: 10px;
}

.search-wrapper {
  position: relative;
  display: flex;
  gap: 8px;
}

input {
  flex: 1;
  padding: 10px 12px;
  font-size: 14px;
  border: 2px solid #444;
  border-radius: 8px;
  background: #2d2d2d;
  color: white;
  transition: all 0.3s;
}

input:focus {
  outline: none;
  border-color: #4CAF50;
}

input::placeholder {
  color: #666;
}

.search-btn {
  padding: 10px 18px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  font-weight: bold;
  white-space: nowrap;
  transition: all 0.3s;
}

.search-btn:hover:not(:disabled) {
  background: #45a049;
  transform: translateY(-2px);
}

.search-btn:disabled {
  background: #555;
  cursor: not-allowed;
  opacity: 0.5;
}

.search-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 90px;
  background: #2d2d2d;
  border: 2px solid #444;
  border-radius: 8px;
  margin-top: 5px;
  max-height: 280px;
  overflow-y: auto;
  z-index: 100;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
}

.result-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 14px;
  cursor: pointer;
  transition: background 0.2s;
  border-bottom: 1px solid #333;
}

.result-item:last-child {
  border-bottom: none;
}

.result-item:hover,
.result-item.highlighted {
  background: #4CAF50;
}

.result-item:hover .stock-name,
.result-item:hover .stock-code,
.result-item.highlighted .stock-name,
.result-item.highlighted .stock-code {
  color: white;
}

.stock-name {
  color: white;
  font-weight: 600;
  font-size: 13px;
  flex: 1;
}

.stock-code {
  color: #888;
  font-size: 12px;
  margin-left: 10px;
}

.no-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 90px;
  background: #2d2d2d;
  border: 2px solid #444;
  border-radius: 8px;
  margin-top: 5px;
  padding: 12px;
  text-align: center;
  color: #888;
  font-size: 13px;
  z-index: 100;
}

.selected-stock {
  padding: 8px 12px;
  background: rgba(76, 175, 80, 0.1);
  border: 2px solid #4CAF50;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.selected-label {
  color: #aaa;
  font-size: 12px;
}

.selected-name {
  color: #4CAF50;
  font-weight: 600;
  font-size: 13px;
}

/* 관심 종목 섹션 */
.watchlist-section {
  flex: 1;
  border-left: 2px solid #333;
  padding-left: 20px;
}

.empty-watchlist {
  text-align: center;
  padding: 20px;
  color: #666;
  font-size: 13px;
}

.watchlist-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.watchlist-btn {
  padding: 8px 14px;
  background: #2d2d2d;
  border: 2px solid #444;
  color: white;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.3s;
  white-space: nowrap;
}

.watchlist-btn:hover {
  background: #353535;
  border-color: #4CAF50;
  transform: translateY(-2px);
}

/* 반응형 */
@media (max-width: 1024px) {
  .stock-search-horizontal {
    grid-template-columns: 1fr;
  }
  
  .watchlist-section {
    border-left: none;
    border-top: 2px solid #333;
    padding-left: 0;
    padding-top: 15px;
  }
}
</style>
