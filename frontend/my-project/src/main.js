import { createApp } from 'vue';
import App from './App.vue';
import router from './router';  // 引入router

const app = createApp(App);
app.use(router);  // 使用router
app.mount('#app');
