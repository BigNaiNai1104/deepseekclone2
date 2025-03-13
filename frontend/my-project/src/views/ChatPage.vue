<template>
  <div class="chat-container">
      <div class="chat-header">
          <h2>聊天</h2>
      </div>
      <div class="chat-body">
          <div v-for="(message, index) in messages" :key="index" class="chat-message">
              <div class="message-bubble">{{ message }}</div>
          </div>
      </div>
      <div class="chat-footer">
          <el-input v-model="userMessage" placeholder="输入消息..." @keyup.enter="sendMessage" />
          <el-button @click="sendMessage">发送</el-button>
      </div>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
      const userMessage = ref('');
      const messages = ref([
          '欢迎来到聊天页面！',
      ]);

      const sendMessage = () => {
          if (userMessage.value.trim() !== '') {
              messages.value.push(userMessage.value);
              userMessage.value = '';
          }
      };

      return {
          userMessage,
          messages,
          sendMessage,
      };
  },
};
</script>

<style scoped>
.chat-container {
  width: 400px;
  margin: 50px auto;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 20px;
  background-color: #fff;
}
.chat-header {
  text-align: center;
  font-size: 1.5em;
}
.chat-body {
  max-height: 300px;
  overflow-y: auto;
  margin-bottom: 20px;
}
.chat-footer {
  display: flex;
  align-items: center;
}
.message-bubble {
  background-color: #f1f1f1;
  padding: 10px;
  border-radius: 20px;
  margin: 5px 0;
}
</style>
