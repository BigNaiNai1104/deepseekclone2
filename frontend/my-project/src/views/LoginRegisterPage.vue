<template>
  <div class="login-register-page">
    <h1>{{ isLogin ? '登录' : '注册' }}</h1>
    <form @submit.prevent="isLogin ? login() : register()">
      <input
        type="text"
        v-model="username"
        placeholder="用户名"
        required
      />
      <input
        type="password"
        v-model="password"
        placeholder="密码"
        required
      />
      <button type="submit">{{ isLogin ? '登录' : '注册' }}</button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
    <p class="toggle-mode">
      {{ isLogin ? '没有账号？' : '已有账号？' }}
      <a href="#" @click.prevent="toggleMode">{{
        isLogin ? '注册' : '登录'
      }}</a>
    </p>
  </div>
</template>

<script>
export default {
  name: 'LoginRegisterPage',
  data() {
    return {
      username: '',
      password: '',
      error: '',
      isLogin: true, // 默认显示登录表单
    };
  },
  methods: {
    // 切换登录/注册模式
    toggleMode() {
      this.isLogin = !this.isLogin;
      this.error = ''; // 清空错误信息
    },

    // 登录逻辑
    async login() {
      try {
        const response = await fetch('/api/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password,
          }),
        });

        if (response.ok) {
          const data = await response.json();
          localStorage.setItem('token', data.access_token); // 存储 token
          alert('登录成功！');
          this.$router.push('/chat'); // 跳转到聊天页面
        } else {
          const errorData = await response.json();
          this.error = errorData.detail || '登录失败，请检查用户名和密码';
        }
      } catch (error) {
        this.error = '网络错误，请稍后重试';
      }
    },

    // 注册逻辑
    async register() {
      try {
        const response = await fetch('/api/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password,
          }),
        });

        if (response.ok) {
          alert('注册成功！');
          this.toggleMode(); // 切换到登录模式
        } else {
          const errorData = await response.json();
          this.error = errorData.detail || '注册失败，请检查用户名和密码';
        }
      } catch (error) {
        this.error = '网络错误，请稍后重试';
      }
    },
  },
};
</script>

<style scoped>
.login-register-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: #1e1e1e;
  color: #ffffff;
}

h1 {
  margin-bottom: 20px;
}

form {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 300px;
}

input {
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ccc;
  background: #2e2e2e;
  color: #ffffff;
}

button {
  padding: 8px 16px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.error {
  color: red;
  margin-top: 12px;
}

.toggle-mode {
  margin-top: 12px;
  color: #ccc;
}

.toggle-mode a {
  color: #007bff;
  text-decoration: none;
}

.toggle-mode a:hover {
  text-decoration: underline;
}
</style>