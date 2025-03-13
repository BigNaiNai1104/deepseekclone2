import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';  // 手动引入CSS文件

const app = createApp(App);
app.use(router);
app.use(ElementPlus);  // 使用ElementPlus
app.mount('#app');
