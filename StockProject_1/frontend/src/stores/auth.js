import { ref, computed } from 'vue'
import axios from 'axios'

const API_BASE = 'http://localhost:8000/api'

// 전역 상태
const user = ref(null)
const token = ref(localStorage.getItem('token') || null)

// axios 기본 설정
if (token.value) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
}

export function useAuth() {
  const isAuthenticated = computed(() => !!token.value)

  // 회원가입
  const register = async (email, password, username) => {
    try {
      const response = await axios.post(`${API_BASE}/auth/register`, {
        email,
        password,
        username
      })

      token.value = response.data.access_token
      user.value = response.data.user
      
      localStorage.setItem('token', token.value)
      axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
      
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.detail || '회원가입 실패' 
      }
    }
  }

  // 로그인
  const login = async (email, password) => {
    try {
      const response = await axios.post(`${API_BASE}/auth/login`, {
        email,
        password
      })

      token.value = response.data.access_token
      user.value = response.data.user
      
      localStorage.setItem('token', token.value)
      axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
      
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.detail || '로그인 실패' 
      }
    }
  }

  // 로그아웃
  const logout = () => {
    token.value = null
    user.value = null
    
    localStorage.removeItem('token')
    delete axios.defaults.headers.common['Authorization']
  }

  // 현재 사용자 정보 가져오기
  const fetchUser = async () => {
    if (!token.value) return

    try {
      const response = await axios.get(`${API_BASE}/auth/me`)
      user.value = response.data
    } catch (error) {
      console.error('사용자 정보 조회 실패:', error)
      logout()
    }
  }

  return {
    user,
    token,
    isAuthenticated,
    register,
    login,
    logout,
    fetchUser
  }
}
