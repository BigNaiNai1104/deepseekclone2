<template>
  <el-tabs v-model="activeTab" @tab-click="handleTabChange">
    <el-tab-pane label="登录" name="login">
      <el-form :model="form" ref="form" status-icon>
        <el-form-item label="用户名" prop="username" :rules="[{ required: true, message: '请输入用户名', trigger: 'blur' }]">
          <el-input v-model="form.username"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password" :rules="[{ required: true, message: '请输入密码', trigger: 'blur' }]">
          <el-input type="password" v-model="form.password"></el-input>
        </el-form-item>
        <el-button type="primary" @click="login">登录</el-button>
      </el-form>
    </el-tab-pane>
    <el-tab-pane label="注册" name="register">
      <el-form :model="form" ref="form" status-icon>
        <el-form-item label="用户名" prop="username" :rules="[{ required: true, message: '请输入用户名', trigger: 'blur' }]">
          <el-input v-model="form.username"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password" :rules="[{ required: true, message: '请输入密码', trigger: 'blur' }]">
          <el-input type="password" v-model="form.password"></el-input>
        </el-form-item>
        <el-button type="primary" @click="register">注册</el-button>
      </el-form>
    </el-tab-pane>
  </el-tabs>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      activeTab: 'login',  // 默认显示登录表单
      form: {
        username: '',
        password: ''
      }
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://localhost:8000/users/login', this.form);
        localStorage.setItem('token', response.data.access_token);  // 保存JWT Token
        this.$router.push('/chat');  // 登录成功后跳转到聊天界面
      } catch (error) {
        this.$message.error('登录失败：' + (error.response ? error.response.data.detail : error.message));  // 显示错误信息
      }
    },

    async register() {
      try {
        await axios.post('http://localhost:8000/users/register', this.form);
        this.$message.success('注册成功，请登录');
        this.activeTab = 'login';  // 注册成功后自动切换到登录界面
      } catch (error) {
        this.$message.error('注册失败：' + (error.response ? error.response.data.detail : error.message));  // 显示错误信息
      }
    },

    handleTabChange(tab) {
      this.form.username = '';
      this.form.password = '';
    }
  }
};
</script>

<style scoped>
/* 可以根据需要调整样式 */
</style>
