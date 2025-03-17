import { createRouter, createWebHistory } from 'vue-router';
import LoginRegisterPage from '@/views/LoginRegisterPage.vue'; // 登录注册页面
import ChatPage from '@/views/ChatPage.vue'; // 聊天页面
import UserSettings from '@/views/UserSettings.vue'; // 用户设置页面
import AdminPage from '@/views/AdminPage.vue'; // 管理员页面

const routes = [
  {
    path: '/',
    redirect: '/login', // 默认重定向到登录页面
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginRegisterPage,
  },
  {
    path: '/chat',
    name: 'Chat',
    component: ChatPage,
    meta: { requiresAuth: true }, // 需要登录
  },
  {
    path: '/settings',
    name: 'Settings',
    component: UserSettings,
    meta: { requiresAuth: true }, // 需要登录
  },
  {
    path: '/admin',
    name: 'Admin',
    component: AdminPage,
    meta: { requiresAdmin: true }, // 需要管理员权限
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL), // 使用 import.meta.env.BASE_URL
  routes,
});

// 路由守卫：检查用户是否登录
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  const isAuthRequired = to.matched.some((record) => record.meta.requiresAuth);
  const isAdminRequired = to.matched.some((record) => record.meta.requiresAdmin);

  if (isAuthRequired && !token) {
    // 如果需要登录但未登录，跳转到登录页面
    next('/login');
  } else if (isAdminRequired && !isAdminUser()) {
    // 如果需要管理员权限但用户不是管理员，跳转到首页
    next('/');
  } else {
    // 否则继续导航
    next();
  }
});

// 模拟检查用户是否是管理员
function isAdminUser() {
  const user = JSON.parse(localStorage.getItem('user'));
  return user && user.is_admin;
}

export default router;