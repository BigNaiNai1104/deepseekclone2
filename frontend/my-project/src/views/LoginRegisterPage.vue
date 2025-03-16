<template>
  <div class="login-page">
    <h1>登录</h1>
    <form @submit.prevent="login">
      <input type="text" v-model="username" placeholder="用户名" required />
      <input type="password" v-model="password" placeholder="密码" required />
      <button type="submit">登录</button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
export default {
  name: 'LoginRegisterPage',
  data() {
    return {
      username: '',
      password: '',
      error: ''
    };
  },
  methods: {
    async login() {
      try {
        const response = await fetch('http://localhost:8000/api/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password
          })
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
    }
  }
};
</script>

<style scoped>
.login-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: #1e1e1e;
  color: #ffffff;
}

form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

input {
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ccc;
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
</style>