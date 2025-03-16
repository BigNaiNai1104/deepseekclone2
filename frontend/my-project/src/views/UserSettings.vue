<template>
  <div class="settings-container">
    <h2>用户设置</h2>
    <el-form :model="settingsForm" label-width="120px">
      <el-form-item label="用户名">
        <el-input v-model="settingsForm.username" placeholder="修改用户名"></el-input>
      </el-form-item>
      <el-form-item label="密码">
        <el-input type="password" v-model="settingsForm.password" placeholder="修改密码"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="saveSettings">保存设置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      settingsForm: {
        username: '',
        password: '',
      },
    };
  },
  methods: {
    async saveSettings() {
      try {
        const response = await axios.put(
          'http://localhost:8000/api/settings',
          this.settingsForm,
          {
            headers: {
              'X-API-Key': 'your-secret-key', // 需要在请求头中添加API密钥
            }
          }
        );
        this.$message.success('设置保存成功');
      } catch (error) {
        this.$message.error('保存失败：' + (error.response ? error.response.data.detail : error.message));
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
</style>