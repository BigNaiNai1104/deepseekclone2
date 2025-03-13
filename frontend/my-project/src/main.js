import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // 或者根据你创建的路径修改

// 引入自定义的 structuredClone 兼容代码
import './utils/structuredClone'; // 根据实际路径修改

const app = createApp(App);
app.use(router);
app.mount('#app');
