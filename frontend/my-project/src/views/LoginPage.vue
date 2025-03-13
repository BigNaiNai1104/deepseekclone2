<template>
    <div class="login-container">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="登录" name="login">
          <el-form :model="loginForm" ref="loginForm" label-width="120px">
            <el-form-item label="用户名" :rules="[{ required: true, message: '请输入用户名', trigger: 'blur' }]">
              <el-input v-model="loginForm.username" placeholder="请输入用户名"></el-input>
            </el-form-item>
            <el-form-item label="密码" :rules="[{ required: true, message: '请输入密码', trigger: 'blur' }]">
              <el-input type="password" v-model="loginForm.password" placeholder="请输入密码"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleLogin">登录</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
  
        <el-tab-pane label="注册" name="register">
          <el-form :model="registerForm" ref="registerForm" label-width="120px">
            <el-form-item label="用户名" :rules="[{ required: true, message: '请输入用户名', trigger: 'blur' }]">
              <el-input v-model="registerForm.username" placeholder="请输入用户名"></el-input>
            </el-form-item>
            <el-form-item label="密码" :rules="[{ required: true, message: '请输入密码', trigger: 'blur' }]">
              <el-input type="password" v-model="registerForm.password" placeholder="请输入密码"></el-input>
            </el-form-item>
            <el-form-item label="确认密码" :rules="[{ required: true, message: '请确认密码', trigger: 'blur' }]">
              <el-input type="password" v-model="registerForm.confirmPassword" placeholder="请确认密码"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleRegister">注册</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  import { ElMessage } from 'element-plus';
  
  export default {
    setup() {
      const router = useRouter();
      const activeTab = ref('login');
      const loginForm = ref({
        username: '',
        password: '',
      });
      const registerForm = ref({
        username: '',
        password: '',
        confirmPassword: '',
      });
  
      const handleLogin = () => {
        // Placeholder for login logic
        if (loginForm.value.username && loginForm.value.password) {
          // Simulate successful login
          ElMessage.success('登录成功');
          router.push('/chat');
        } else {
          ElMessage.error('请填写完整的登录信息');
        }
      };
  
      const handleRegister = () => {
        // Placeholder for register logic
        if (registerForm.value.password !== registerForm.value.confirmPassword) {
          ElMessage.error('密码不匹配');
        } else {
          ElMessage.success('注册成功');
          router.push('/chat');
        }
      };
  
      return {
        activeTab,
        loginForm,
        registerForm,
        handleLogin,
        handleRegister,
      };
    },
  };
  </script>
  
  <style scoped>
  .login-container {
    width: 400px;
    margin: 100px auto;
  }
  </style>
  