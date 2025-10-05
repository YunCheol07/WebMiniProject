<template>
  <div class="stock-search">
    <h2>📈 주식 검색</h2>
    
    <div class="search-box">
      <input 
        v-model="searchQuery" 
        @input="handleSearchInput"
        @keyup.enter="selectFirstResult"
        @keydown.down="highlightNext"
        @keydown.up="highlightPrev"
        @focus="showResults = true"
        placeholder="종목명 또는 종목코드 입력 (예: 삼성전자, 005930)"
        autocomplete="off"
        ref="searchInput"
      />
      <button @click="searchStock" :disabled="!selectedStock">
        🔍 조회
      </button>
    </div>

    <!-- 자동완성 결과 -->
    <div v-if="showResults && searchResults.length > 0" class="search-results">
      <div 
        v-for="(stock, index) in searchResults" 
        :key="stock.stock_code"
        :class="['result-item', { highlighted: highlightedIndex === index }]"
        @click="selectStock(stock)"
        @mouseenter="highlightedIndex = index"
      >
        <div class="stock-info">
          <span class="stock-name" v-html="highlightText(stock.stock_name)"></span>
          <span class="stock-code">{{ stock.stock_code }}</span>
        </div>
      </div>
    </div>

    <div v-if="showResults && searchQuery && searchResults.length === 0" class="no-results">
      검색 결과가 없습니다
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
const highlightedIndex = ref(-1)
const searchInput = ref(null)

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
  }, 200) // 200ms 디바운싱
}

// 검색어 하이라이트
const highlightText = (text) => {
  if (!searchQuery.value) return text
  
  const query = searchQuery.value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  const regex = new RegExp(`(${query})`, 'gi')
  return text.replace(regex, '<mark>$1</mark>')
}

// 키보드 네비게이션
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

const selectStock = (stock) => {
  selectedStock.value = stock
  searchQuery.value = `${stock.stock_name} (${stock.stock_code})`
  showResults.value = false
  highlightedIndex.value = -1
  emit('search', stock.stock_code, stock.stock_name)
}

const selectFirstResult = () => {
  if (highlightedIndex.value >= 0 && searchResults.value[highlightedIndex.value]) {
    selectStock(searchResults.value[highlightedIndex.value])
  } else if (searchResults.value.length > 0) {
    selectStock(searchResults.value[0])
  }
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

document.addEventListener('click', (e) => {
  if (!e.target.closest('.stock-search')) {
    showResults.value = false
  }
})
</script>

<style scoped>
/* 스타일은 동일, market-badge만 제거 */
mark {
  background-color: #4CAF50;
  color: white;
  padding: 2px 4px;
  border-radius: 3px;
  font-weight: bold;
}

.result-item.highlighted {
  background: #4CAF50 !important;
}

.result-item.highlighted .stock-name,
.result-item.highlighted .stock-code {
  color: white;
}

.stock-search {
  padding: 20px;
  background: #1e1e1e;
  border-radius: 10px;
  margin-bottom: 20px;
  position: relative;
}

h2 {
  color: #4CAF50;
  margin-bottom: 10px;
}

.search-box {
  display: flex;
  gap: 10px;
  margin: 20px 0;
  position: relative;
}

input {
  flex: 1;
  padding: 14px;
  font-size: 16px;
  border: 2px solid #444;
  border-radius: 8px;
  background: #2d2d2d;
  color: white;
  transition: border-color 0.3s;
}

input:focus {
  outline: none;
  border-color: #4CAF50;
}

button {
  padding: 14px 24px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  white-space: nowrap;
  transition: all 0.3s;
}

button:hover:not(:disabled) {
  background: #45a049;
}

button:disabled {
  background: #555;
  cursor: not-allowed;
}

.search-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: #2d2d2d;
  border: 2px solid #444;
  border-radius: 8px;
  margin-top: -10px;
  max-height: 300px;
  overflow-y: auto;
  z-index: 100;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
}

.result-item {
  padding: 12px 16px;
  cursor: pointer;
  transition: background 0.2s;
  border-bottom: 1px solid #333;
}

.result-item:last-child {
  border-bottom: none;
}

.result-item:hover {
  background: #353535;
}

.stock-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stock-name {
  font-size: 15px;
  font-weight: 600;
  color: white;
}

.stock-code {
  font-size: 13px;
  color: #888;
}

.no-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: #2d2d2d;
  border: 2px solid #444;
  border-radius: 8px;
  margin-top: -10px;
  padding: 16px;
  text-align: center;
  color: #888;
  z-index: 100;
}

.popular-stocks {
  margin-top: 30px;
}

.popular-stocks h3 {
  margin-bottom: 10px;
  color: #aaa;
  font-size: 14px;
}

.popular-stocks button {
  min-width: 100px;
  margin: 5px;
  background: #555;
  padding: 10px 16px;
}

.popular-stocks button:hover {
  background: #666;
}
</style>
