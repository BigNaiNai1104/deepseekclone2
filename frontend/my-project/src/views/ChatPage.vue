<template>
  <div class="app-container">
    <!-- 侧边栏 -->
    <div class="sidebar">
      <!-- 添加标题 -->
      <div class="sidebar-title">
        <h1>DeepseekClone</h1>
      </div>
      <div class="sidebar-header">
        <h2>对话历史</h2>
      </div>
      <div class="chat-list">
        <!-- 遍历历史记录 -->
        <div
          v-for="chat in chatHistory"
          :key="chat.id"
          class="chat-item"
          :class="{ active: chat.id === activeChatId }"
          @click="switchChat(chat)"
        >
          <span>{{ chat.title }}</span>
        </div>
      </div>
      <div class="sidebar-buttons">
        <button class="button-text" @click="newChat">开启新对话</button>
        <button class="button-text" @click="openSettings">设置</button>
        <button class="button-text" @click="logout">退出</button>
      </div>
    </div>

    <!-- 主内容区域 -->
    <div class="main-content">
      <div class="messages">
        <!-- 显示当前对话的消息 -->
        <div v-for="(msg, index) in messages" :key="index" class="message">
          <div class="avatar">{{ msg.sender === 'user' ? '👤' : '🤖' }}</div>
          <div class="bubble">
            <p>{{ msg.text }}</p>
          </div>
        </div>
      </div>
      <div class="input-area">
        <input
          type="text"
          v-model="message"
          placeholder="请输入消息..."
          @keyup.enter="sendMessage"
        />
        <button @click="sendMessage">发送</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ChatPage',
  data() {
    return {
      message: '', // 用于绑定输入框的内容
      messages: [], // 当前对话的消息列表
      chatHistory: [], // 历史记录（所有对话）
      activeChatId: null, // 当前选中的对话 ID
      chatCounter: 1 // 用于生成对话标题的计数器
    };
  },
  methods: {
    // 开启新对话
    newChat() {
      // 创建一个新的对话对象
      const newChat = {
        id: Date.now(), // 使用时间戳作为唯一 ID
        title: `对话${this.chatCounter}`, // 格式化标题为“对话1”、“对话2”等
        messages: [] // 初始化为空的消息列表
      };

      // 将新对话添加到历史记录中
      this.chatHistory.push(newChat);

      // 更新对话计数器
      this.chatCounter++;

      // 切换到新对话
      this.switchChat(newChat);

      // 提示用户新对话已创建
      alert('已开启新对话');
    },

    // 切换对话
    switchChat(chat) {
      // 设置当前选中的对话 ID
      this.activeChatId = chat.id;

      // 将当前对话的消息设置为选中对话的消息
      this.messages = chat.messages;
    },

    // 发送消息
    sendMessage() {
      if (this.message.trim() === '') return; // 如果输入框为空，则不发送

      // 将用户输入的消息添加到当前对话的消息列表中
      const activeChat = this.chatHistory.find(chat => chat.id === this.activeChatId);
      if (activeChat) {
        activeChat.messages.push({ text: this.message, sender: 'user' });
      }

      // 清空输入框
      this.message = '';

      // 这里可以添加发送消息到后端的逻辑
      // 例如：this.sendToBackend(this.message);
    },

    // 打开设置
    openSettings() {
      alert('打开设置');
      // 在这里实现打开设置的逻辑
    },

    // 退出登录
    logout() {
      // 清除登录状态（例如清除 token）
      localStorage.removeItem('auth_token'); // 假设 token 存储在 localStorage 中

      // 跳转到登录注册界面
      this.$router.push('/login'); // 假设登录注册界面的路由是 '/login'
    }
  },
  mounted() {
    // 初始化一个默认对话（可选）
    this.newChat();
  }
};
</script>

<style scoped>
.app-container {
  display: flex;
  height: 100vh;
  background: var(--bg-color);
  color: var(--text-color);
}

/* 侧边栏样式 */
.sidebar {
  width: 280px;
  background: #1e1e1e; /* 暗色背景 */
  border-right: 1px solid #333; /* 暗色边框 */
  padding: 16px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

/* 标题样式 */
.sidebar-title {
  margin-bottom: 24px;
  color: #ffffff; /* 白色文字 */
}

.sidebar-title h1 {
  font-size: 24px;
  font-weight: bold;
  margin: 0;
}

.sidebar-header {
  margin-bottom: 16px;
  color: #ffffff; /* 白色文字 */
}

.chat-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.chat-item {
  display: flex;
  flex-direction: column;
  padding: 8px;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;
  color: #ffffff; /* 白色文字 */
}

.chat-item:hover {
  background: rgba(255, 255, 255, 0.05); /* 悬停时的浅色背景 */
}

.chat-item.active {
  background: rgba(0, 123, 255, 0.3); /* 更柔和的高亮颜色 */
}

.sidebar-buttons {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 16px;
}

.button-text {
  font-size: 14px;
  color: #ffffff; /* 白色文字 */
  padding: 8px 12px;
  background-color: #333; /* 暗色按钮背景 */
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.button-text:hover {
  background-color: #444; /* 悬停时的按钮背景 */
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 24px;
  background: var(--bg-color);
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  margin-bottom: 16px;
  background: var(--bg-color);
}

.message {
  display: flex;
  align-items: flex-start;
  margin-bottom: 16px;
}

.avatar {
  font-size: 24px;
  margin-right: 8px;
}

.bubble {
  background: var(--bubble-bg);
  padding: 8px 12px;
  border-radius: 8px;
  max-width: 70%;
}

.input-area {
  display: flex;
  gap: 12px;
  padding: 16px;
  background: var(--bg-color);
  border-top: 1px solid var(--sidebar-border);
}

input {
  flex: 1;
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
</style>