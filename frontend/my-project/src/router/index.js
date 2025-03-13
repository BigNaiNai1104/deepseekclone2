import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '@/views/LoginRegisterPage.vue';
import ChatPage from '@/views/ChatPage.vue';
import UserSettings from '@/views/UserSettings.vue';

const routes = [
  {
    path: '/',
    redirect: '/login' // 默认重定向到登录页面
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage
  },
  {
    path: '/chat',
    name: 'Chat',
    component: ChatPage
  },
  {
    path: '/settings',
    name: 'Settings',
    component: UserSettings
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;
