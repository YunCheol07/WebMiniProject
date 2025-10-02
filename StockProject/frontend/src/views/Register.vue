<template>
  <div class="register-page">
    <div class="register-container">
      <div class="register-header">
        <h1>🏦 회원가입</h1>
        <p>새 계정 만들기</p>
      </div>

      <form @submit.prevent="handleRegister" class="register-form">
        <div class="form-group">
          <label for="username">이름</label>
          <input
            id="username"
            v-model="formData.username"
            type="text"
            placeholder="홍길동"
            required
            autocomplete="name"
          />
        </div>

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
            placeholder="최소 6자 이상"
            required
            minlength="6"
            autocomplete="new-password"
          />
        </div>

        <div class="form-group">
          <label for="password-confirm">비밀번호 확인</label>
          <input
            id="password-confirm"
            v-model="formData.passwordConfirm"
            type="password"
            placeholder="비밀번호 재입력"
            required
            minlength="6"
            autocomplete="new-password"
          />
        </div>

        <div v-if="error" class="error-message">
          <span>{{ error }}</span>
        </div>

        <button type="submit" class="register-btn" :disabled="loading">
          {{ loading ? '가입 중...' : '회원가입' }}
        </button>
      </form>

      <div class="footer">
        <p>이미 계정이 있으신가요?</p>
        <router-link to="/login" class="login-link">
          로그인하기
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
const { register } = useAuth()

const loading = ref(false)
const error = ref('')

const formData = ref({
  username: '',
  email: '',
  password: '',
  passwordConfirm: ''
})

const handleRegister = async () => {
  loading.value = true
  error.value = ''

  // 비밀번호 확인
  if (formData.value.password !== formData.value.passwordConfirm) {
    error.value = '비밀번호가 일치하지 않습니다'
    loading.value = false
    return
  }

  try {
    const result = await register(
      formData.value.email,
      formData.value.password,
      formData.value.username
    )

    if (result.success) {
      router.push('/')
    } else {
      error.value = result.message
    }
  } catch (err) {
    error.value = '회원가입 중 오류가 발생했습니다.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.register-container {
  background: #1e1e1e;
  padding: 40px;
  border-radius: 20px;
  width: 100%;
  max-width: 450px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.register-header {
  text-align: center;
  margin-bottom: 40px;
}

.register-header h1 {
  color: #4CAF50;
  font-size: 32px;
  margin-bottom: 10px;
}

.register-header p {
  color: #aaa;
  font-size: 16px;
}

.register-form {
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 20px;
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

.register-btn {
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

.register-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
}

.register-btn:disabled {
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

.login-link {
  display: inline-block;
  color: #4CAF50;
  font-size: 16px;
  font-weight: bold;
  text-decoration: none;
  transition: color 0.3s;
}

.login-link:hover {
  color: #45a049;
  text-decoration: underline;
}
</style>
