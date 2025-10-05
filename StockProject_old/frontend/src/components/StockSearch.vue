<template>
  <div class="stock-search">
    <h2>📈 주식 검색</h2>
    
    <div class="search-box">
      <input 
        v-model="searchInput" 
        @keyup.enter="searchStock"
        @input="handleInput"
        placeholder="종목명 또는 종목코드 입력 (예: 삼성전자 또는 005930)"
        list="stock-suggestions"
      />
      <datalist id="stock-suggestions">
        <option v-for="(code, name) in filteredStocks" :key="code" :value="name">
          {{ name }} ({{ code }})
        </option>
      </datalist>
      <button @click="searchStock">🔍 조회</button>
    </div>

    <div class="popular-stocks">
      <h3>주요 종목:</h3>
      <button 
        v-for="(name, code) in popularStocks" 
        :key="code"
        @click="selectStock(code)"
      >
        {{ name }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, defineEmits } from 'vue';

const emit = defineEmits(['search']);

const searchInput = ref('삼성전자');

// 주요 종목 매핑 (종목코드: 종목명)
const popularStocks = {
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
};

// 종목명으로 검색을 위한 역매핑 (종목명: 종목코드)
const stockNameToCode = Object.fromEntries(
  Object.entries(popularStocks).map(([code, name]) => [name, code])
);

// 입력값 기반 필터링된 종목 리스트
const filteredStocks = computed(() => {
  if (!searchInput.value) return popularStocks;
  
  const input = searchInput.value.toLowerCase();
  return Object.fromEntries(
    Object.entries(popularStocks).filter(([code, name]) => 
      name.toLowerCase().includes(input) || code.includes(input)
    )
  );
});

// 입력 처리
const handleInput = () => {
  // 자동완성을 위한 처리 (필요시 추가 로직)
};

// 검색 실행
const searchStock = () => {
  let code = searchInput.value.trim();
  
  // 1. 종목명으로 입력한 경우 → 종목코드로 변환
  if (stockNameToCode[code]) {
    code = stockNameToCode[code];
  }
  // 2. 부분 매칭 검색 (예: "삼성" 입력 시 "삼성전자" 찾기)
  else if (!/^\d{6}$/.test(code)) {
    const matchedName = Object.keys(stockNameToCode).find(name => 
      name.includes(code)
    );
    if (matchedName) {
      code = stockNameToCode[matchedName];
    } else {
      alert('종목을 찾을 수 없습니다. 정확한 종목명 또는 6자리 코드를 입력하세요.');
      return;
    }
  }
  
  // 3. 종목코드 검증
  if (code && code.length === 6) {
    emit('search', code);
  } else {
    alert('올바른 6자리 종목코드 또는 종목명을 입력하세요');
  }
};

// 주요 종목 버튼 클릭
const selectStock = (code) => {
  searchInput.value = popularStocks[code];
  emit('search', code);
};
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
  margin-bottom: 10px;
}

.search-box {
  display: flex;
  gap: 10px;
  margin: 20px 0;
}

input {
  flex: 1;
  padding: 12px;
  font-size: 16px;
  border: 2px solid #444;
  border-radius: 5px;
  background: #2d2d2d;
  color: white;
}

input::placeholder {
  color: #888;
}

button {
  padding: 12px 24px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  white-space: nowrap;
}

button:hover {
  background: #45a049;
}

.popular-stocks {
  margin-top: 20px;
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
