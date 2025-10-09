<template>
  <div class="stock-search">
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
          placeholder="종목명 또는 종목코드 입력 (예: 삼성전자, 005930)"
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
      <span class="selected-label">선택된 종목:</span>
      <span class="selected-name">{{ selectedStock.stock_name }} ({{ selectedStock.stock_code }})</span>
    </div>

    <div class="popular-stocks">
      <h3>주요 종목:</h3>
      <button 
        v-for="(name, code) in popularStocks" 
        :key="code"
        @click="quickSelect(code, name)"
      >
        {{ name }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, defineEmits } from 'vue'
import axios from 'axios'

const emit = defineEmits(['search'])

const API_BASE = 'http://localhost:8000/api'

const searchQuery = ref('')
const searchResults = ref([])
const showResults = ref(false)
const selectedStock = ref(null)
const searchInput = ref(null)
const highlightedIndex = ref(-1)

const popularStocks = {
  '005930': '삼성전자',
  '000660': 'SK하이닉스',
  '035420': 'NAVER',
  '035720': '카카오',
  '005380': '현대차'
}

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

// 키보드 네비게이션 - 아래 방향키
const highlightNext = () => {
  if (searchResults.value.length > 0) {
    highlightedIndex.value = Math.min(
      highlightedIndex.value + 1,
      searchResults.value.length - 1
    )
  }
}

// 키보드 네비게이션 - 위 방향키
const highlightPrev = () => {
  highlightedIndex.value = Math.max(highlightedIndex.value - 1, -1)
}

// Enter 키 처리
const handleEnterKey = () => {
  // 하이라이트된 항목이 있으면 선택
  if (highlightedIndex.value >= 0 && searchResults.value[highlightedIndex.value]) {
    selectStock(searchResults.value[highlightedIndex.value])
    searchStock()
  } 
  // 하이라이트 없고 검색 결과가 있으면 첫 번째 항목 선택
  else if (searchResults.value.length > 0) {
    selectStock(searchResults.value[0])
    searchStock()
  }
  // 이미 선택된 종목이 있으면 바로 조회
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

// 외부 클릭 시 검색 결과 숨기기
document.addEventListener('click', (e) => {
  if (!e.target.closest('.stock-search')) {
    showResults.value = false
  }
})
</script>

<style scoped>
.stock-search {
  padding: 20px;
  background: #1e1e1e;
  border-radius: 10px;
  margin-bottom: 20px;
}

h2 {
  color: #4CAF50;
  margin-bottom: 15px;
  font-size: 22px;
}

.search-box {
  margin-bottom: 20px;
}

.search-wrapper {
  position: relative;
  display: flex;
  gap: 10px;
}

input {
  flex: 1;
  padding: 14px 16px;
  font-size: 16px;
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
  padding: 14px 24px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
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

/* 자동완성 결과 */
.search-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 120px;
  background: #2d2d2d;
  border: 2px solid #444;
  border-radius: 8px;
  margin-top: 5px;
  max-height: 300px;
  overflow-y: auto;
  z-index: 100;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
}

.result-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
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
  font-size: 15px;
  flex: 1;
}

.stock-code {
  color: #888;
  font-size: 13px;
  margin-left: 10px;
}

.no-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 120px;
  background: #2d2d2d;
  border: 2px solid #444;
  border-radius: 8px;
  margin-top: 5px;
  padding: 16px;
  text-align: center;
  color: #888;
  z-index: 100;
}

/* 선택된 종목 표시 */
.selected-stock {
  padding: 12px 16px;
  background: rgba(76, 175, 80, 0.1);
  border: 2px solid #4CAF50;
  border-radius: 8px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.selected-label {
  color: #aaa;
  font-size: 14px;
}

.selected-name {
  color: #4CAF50;
  font-weight: 600;
  font-size: 16px;
}

/* 주요 종목 */
.popular-stocks {
  margin-top: 30px;
}

.popular-stocks h3 {
  margin-bottom: 12px;
  color: #aaa;
  font-size: 14px;
  font-weight: 600;
}

.popular-stocks button {
  min-width: 100px;
  margin: 5px;
  background: #2d2d2d;
  border: 2px solid #444;
  color: white;
  padding: 10px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}

.popular-stocks button:hover {
  background: #353535;
  border-color: #4CAF50;
  transform: translateY(-2px);
}
</style>
