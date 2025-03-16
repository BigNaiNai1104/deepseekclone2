<template>
  <div class="settings-container">
    <h2>修改密码</h2>
    <el-form :model="passwordForm" label-width="120px">
      <el-form-item label="旧密码">
        <el-input
          type="password"
          v-model="passwordForm.oldPassword"
          placeholder="请输入旧密码"
        ></el-input>
      </el-form-item>
      <el-form-item label="新密码">
        <el-input
          type="password"
          v-model="passwordForm.newPassword"
          placeholder="请输入新密码"
        ></el-input>
      </el-form-item>
      <el-form-item label="确认新密码">
        <el-input
          type="password"
          v-model="passwordForm.confirmPassword"
          placeholder="请再次输入新密码"
        ></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="changePassword">保存修改</el-button>
      </el-form-item>
    </el-form>
    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="success" class="success">{{ success }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      passwordForm: {
        oldPassword: '',
        newPassword: '',
        confirmPassword: '',
      },
      error: '',
      success: '',
    };
  },
  methods: {
    async changePassword() {
      // 验证新密码和确认密码是否一致
      if (this.passwordForm.newPassword !== this.passwordForm.confirmPassword) {
        this.error = '新密码和确认密码不一致';
        return;
      }

      try {
        const token = localStorage.getItem('token');
        if (!token) {
          this.error = '用户未登录';
          return;
        }

        const response = await axios.post(
          'http://localhost:8000/api/change-password',
          {
            old_password: this.passwordForm.oldPassword,
            new_password: this.passwordForm.newPassword,
          },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (response.status === 200) {
          this.success = '密码修改成功';
          this.error = '';
          this.passwordForm = {
            oldPassword: '',
            newPassword: '',
            confirmPassword: '',
          };
        }
      } catch (error) {
        this.error = error.response?.data?.detail || '密码修改失败';
      }
    },
  },
};
</script>

<style scoped>
.settings-container {
  width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #fff;
}

.error {
  color: red;
  margin-top: 12px;
}

.success {
  color: green;
  margin-top: 12px;
}
</style>