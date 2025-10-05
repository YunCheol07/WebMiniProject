<template>
  <div class="watchlist-panel">
    <h3>⭐ 관심 종목</h3>
    
    <div v-if="!isAuthenticated" class="login-required">
      <p>로그인 후 이용 가능합니다</p>
    </div>

    <div v-else-if="loading" class="loading">
      <p>로딩 중...</p>
    </div>

    <div v-else-if="watchlist.length === 0" class="empty-state">
      <p>관심 종목이 없습니다</p>
      <p class="help-text">종목 조회 후 ❤️ 버튼을 눌러 추가하세요</p>
    </div>

    <div v-else class="watchlist-grid">
      <div 
        v-for="item in watchlist" 
        :key="item.watchlist_id"
        class="watchlist-item"
        @click="selectStock(item)"
      >
        <div class="item-header">
          <span class="stock-name">{{ item.stock_name }}</span>
          <button 
            @click.stop="removeFromWatchlist(item)"
            class="remove-btn"
            title="삭제"
          >
            ✕
          </button>
        </div>
        <span class="stock-code">{{ item.stock_code }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, defineEmits } from 'vue'
import axios from 'axios'
import { useAuth } from '../stores/auth'

const emit = defineEmits(['select'])

const API_BASE = 'http://localhost:8000/api'

const { isAuthenticated } = useAuth()

const watchlist = ref([])
const loading = ref(false)

const fetchWatchlist = async () => {
  const token = localStorage.getItem('token')
  if (!token) return

  loading.value = true

  try {
    const response = await axios.get(`${API_BASE}/watchlist`, {
      headers: { Authorization: `Bearer ${token}` }
    })

    if (response.data.success) {
      watchlist.value = response.data.watchlist
    }
  } catch (error) {
    console.error('관심 종목 조회 실패:', error)
  } finally {
    loading.value = false
  }
}

const selectStock = (item) => {
  emit('select', item.stock_code, item.stock_name)
}

const removeFromWatchlist = async (item) => {
  if (!confirm(`${item.stock_name}을(를) 관심 종목에서 삭제하시겠습니까?`)) {
    return
  }

  const token = localStorage.getItem('token')

  try {
    const response = await axios.delete(
      `${API_BASE}/watchlist/${item.stock_code}`,
      {
        headers: { Authorization: `Bearer ${token}` }
      }
    )

    if (response.data.success) {
      watchlist.value = watchlist.value.filter(
        w => w.watchlist_id !== item.watchlist_id
      )
    }
  } catch (error) {
    console.error('관심 종목 삭제 실패:', error)
    alert('삭제에 실패했습니다')
  }
}

onMounted(() => {
  if (isAuthenticated.value) {
    fetchWatchlist()
  }
})

// 외부에서 새로고침할 수 있도록 노출
defineExpose({ fetchWatchlist })
</script>

<style scoped>
.watchlist-panel {
  background: #1e1e1e;
  padding: 20px;
  border-radius: 10px;
  margin-top: 20px;
}

h3 {
  color: #4CAF50;
  margin-bottom: 15px;
  font-size: 18px;
}

.login-required,
.loading,
.empty-state {
  text-align: center;
  padding: 30px;
  color: #888;
}

.help-text {
  font-size: 14px;
  color: #666;
  margin-top: 10px;
}

.watchlist-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 12px;
}

.watchlist-item {
  background: #2d2d2d;
  padding: 15px;
  border-radius: 8px;
  border: 2px solid #444;
  cursor: pointer;
  transition: all 0.3s;
}

.watchlist-item:hover {
  border-color: #4CAF50;
  background: #353535;
  transform: translateY(-2px);
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}

.stock-name {
  color: white;
  font-weight: 600;
  font-size: 15px;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.stock-code {
  color: #888;
  font-size: 13px;
}

.remove-btn {
  background: none;
  border: none;
  color: #888;
  cursor: pointer;
  font-size: 18px;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s;
}

.remove-btn:hover {
  background: #f44336;
  color: white;
}
</style>
