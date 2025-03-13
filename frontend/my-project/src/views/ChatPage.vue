<template>
  <div class="chat-container">
    <el-row class="chat-row">
      <el-col :span="24">
        <el-input
          v-model="message"
          placeholder="请输入消息"
          @keyup.enter="sendMessage"
          clearable
        ></el-input>
      </el-col>
      <el-col :span="24">
        <el-button @click="sendMessage" type="primary">发送</el-button>
      </el-col>
    </el-row>
    <div v-for="(msg, index) in chatHistory" :key="index" class="chat-message">
      <div v-if="msg.role === 'user'" class="user-message">{{ msg.content }}</div>
      <div v-else class="assistant-message">{{ msg.content }}</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      message: '',
      chatHistory: [],
      sessionId: localStorage.getItem('session_id') || null, // 从本地存储获取session_id
    };
  },
  methods: {
    async sendMessage() {
      if (this.message.trim() === '') return; // 防止发送空消息

      try {
        const response = await axios.post(
          'http://localhost:8000/api/chat',
          {
            message: this.message,
            session_id: this.sessionId
          },
          {
            headers: {
              'X-API-Key': 'your-secret-key', // 需要在请求头中添加API密钥
            }
          }
        );
        const responseData = response.data;

        // 更新会话ID，保持会话状态
        this.sessionId = responseData.session_id;
        localStorage.setItem('session_id', this.sessionId);

        // 将用户消息和助手消息加入聊天历史
        this.chatHistory.push({ role: 'user', content: this.message });
        this.chatHistory.push({
          role: 'assistant',
          content: responseData.reply,
        });

        this.message = ''; // 清空输入框
      } catch (error) {
        this.$message.error('消息发送失败：' + (error.response ? error.response.data.detail : error.message));
      }
    },
  },
};
</script>

<style scoped>
.chat-container {
  margin-top: 20px;
}

.chat-row {
  margin-bottom: 10px;
}

.chat-message {
  margin: 5px 0;
}

.user-message {
  color: blue;
}

.assistant-message {
  color: green;
}
</style>
