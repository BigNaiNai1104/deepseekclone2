import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '@/views/LoginRegisterPage.vue'
import ChatPage from '@/views/ChatPage.vue'
import UserSettings from '@/views/UserSettings.vue'
import AdminPage from '@/views/AdminPage.vue'  // 假设你有一个管理员页面

const routes = [
  {
    path: '/',
    redirect: '/login'  // 默认重定向到登录页面
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage
  },
  {
    path: '/chat',
    name: 'Chat',
    component: ChatPage,
    meta: { requiresAuth: true }  // 需要登录
  },
  {
    path: '/settings',
    name: 'Settings',
    component: UserSettings,
    meta: { requiresAuth: true }  // 需要登录
  },
  {
    path: '/admin',
    name: 'Admin',
    component: AdminPage,
    meta: { requiresAdmin: true }  // 需要管理员权限
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// 路由守卫：检查用户是否登录
router.beforeEach((to, from, next) => {
  const isLoggedIn = localStorage.getItem('token')
  const isAdmin = localStorage.getItem('is_admin') === 'true'

  if (to.meta.requiresAuth && !isLoggedIn) {
    // 如果需要登录但用户未登录，跳转到登录页面
    next('/login')
  } else if (to.meta.requiresAdmin && !isAdmin) {
    // 如果需要管理员权限但用户不是管理员，跳转到聊天页面
    next('/chat')
  } else {
    // 否则继续导航
    next()
  }
})

export default router