<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-header">
        <h1>🏦 주식 대시보드</h1>
        <p>로그인하여 계속하기</p>
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="email">이메일</label>
          <input
            id="email"
            v-model="formData.email"
            type="email"
            placeholder="email@example.com"
            required
            autocomplete="email"
          />
        </div>

        <div class="form-group">
          <label for="password">비밀번호</label>
          <input
            id="password"
            v-model="formData.password"
            type="password"
            placeholder="비밀번호 입력"
            required
            minlength="6"
            autocomplete="current-password"
          />
        </div>

        <div v-if="error" class="error-message">
          <span>{{ error }}</span>
        </div>

        <button type="submit" class="login-btn" :disabled="loading">
          {{ loading ? '로그인 중...' : '로그인' }}
        </button>
      </form>

      <div class="footer">
        <p>계정이 없으신가요?</p>
        <router-link to="/register" class="register-link">
          회원가입하기
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '../stores/auth'

const router = useRouter()
const { login } = useAuth()

const loading = ref(false)
const error = ref('')

const formData = ref({
  email: '',
  password: ''
})

const handleLogin = async () => {
  loading.value = true
  error.value = ''

  try {
    const result = await login(formData.value.email, formData.value.password)

    if (result.success) {
      router.push('/')
    } else {
      error.value = result.message
    }
  } catch (err) {
    error.value = '로그인 중 오류가 발생했습니다.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-container {
  background: #1e1e1e;
  padding: 40px;
  border-radius: 20px;
  width: 100%;
  max-width: 450px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.login-header h1 {
  color: #4CAF50;
  font-size: 32px;
  margin-bottom: 10px;
}

.login-header p {
  color: #aaa;
  font-size: 16px;
}

.login-form {
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 25px;
}

label {
  display: block;
  color: #aaa;
  font-size: 14px;
  margin-bottom: 8px;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 14px;
  background: #2d2d2d;
  border: 2px solid #444;
  border-radius: 10px;
  color: white;
  font-size: 16px;
  transition: all 0.3s;
}

input:focus {
  outline: none;
  border-color: #4CAF50;
  background: #353535;
}

.error-message {
  background: rgba(244, 67, 54, 0.1);
  border: 1px solid #f44336;
  color: #f44336;
  padding: 14px;
  border-radius: 10px;
  margin-bottom: 20px;
  text-align: center;
  font-size: 14px;
}

.login-btn {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
}

.login-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
}

.login-btn:disabled {
  background: #555;
  cursor: not-allowed;
  box-shadow: none;
  transform: none;
}

.footer {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid #333;
}

.footer p {
  color: #aaa;
  font-size: 14px;
  margin-bottom: 10px;
}

.register-link {
  display: inline-block;
  color: #4CAF50;
  font-size: 16px;
  font-weight: bold;
  text-decoration: none;
  transition: color 0.3s;
}

.register-link:hover {
  color: #45a049;
  text-decoration: underline;
}
</style>
