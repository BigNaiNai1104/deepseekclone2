import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '@/views/LoginPage.vue';
import ChatPage from '@/views/ChatPage.vue';
import UserSettings from '@/views/UserSettings.vue';

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: LoginPage },
  { path: '/chat', component: ChatPage },
  { path: '/settings', component: UserSettings },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
