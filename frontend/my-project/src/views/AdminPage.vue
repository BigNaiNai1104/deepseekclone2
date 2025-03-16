<template>
    <div class="admin-login">
      <h1>管理员登录</h1>
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
    name: 'AdminLogin',
    data() {
      return {
        username: '',
        password: '',
        error: ''
      };
    },
    methods: {
      login() {
        // 模拟管理员登录逻辑
        if (this.username === 'admin' && this.password === 'admin123') {
          localStorage.setItem('isAdmin', 'true'); // 标记为管理员
          this.$router.push('/admin/dashboard'); // 跳转到管理员仪表盘
        } else {
          this.error = '用户名或密码错误';
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .admin-login {
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