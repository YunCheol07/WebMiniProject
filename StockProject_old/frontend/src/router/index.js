import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import StockDashboard from '../views/StockDashboard.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: Login,
      meta: { requiresGuest: true }
    },
    {
      path: '/register',
      name: 'register',
      component: Register,
      meta: { requiresGuest: true }
    },
    {
      path: '/',
      name: 'dashboard',
      component: StockDashboard,
      meta: { requiresAuth: true }
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/login'
    }
  ]
})

// 라우터 가드 (인증 체크)
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const isAuthenticated = !!token

  // 인증이 필요한 페이지
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  }
  // 로그인한 사용자는 로그인/회원가입 페이지 접근 불가
  else if (to.meta.requiresGuest && isAuthenticated) {
    next('/')
  }
  else {
    next()
  }
})

export default router
