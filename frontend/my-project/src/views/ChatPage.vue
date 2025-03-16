<template>
  <div class="app-container">
    <!-- 侧边栏 -->
    <div class="sidebar">
      <div class="sidebar-title">
        <h1>DeepseekClone</h1>
      </div>
      <div class="sidebar-header">
        <h2>对话历史</h2>
      </div>
      <div class="chat-list">
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
        <!-- 管理员按钮 -->
        <button
          v-if="isAdmin"
          class="button-text"
          @click="goToAdminPage"
        >
          管理员
        </button>
      </div>
    </div>

    <!-- 主内容区域 -->
    <div class="main-content">
      <div class="messages">
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
      message: '', // 用户输入的消息
      messages: [], // 当前对话的消息列表
      chatHistory: [], // 对话历史
      activeChatId: null, // 当前选中的对话 ID
      isAdmin: false, // 是否是管理员
    };
  },
  methods: {
    async checkAdminStatus() {
      // 调用后端接口检查用户是否是管理员
      try {
        const token = localStorage.getItem('token'); // 从本地存储获取 Token
        if (!token) {
          console.error('未找到 Token');
          this.logout(); // 如果未找到 Token，跳转到登录页面
          return;
        }

        const response = await fetch('http://localhost:8000/api/me', {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${token}`, // 携带 Token
          },
        });

        if (!response.ok) {
          // 如果返回 401 或其他错误状态码
          if (response.status === 401) {
            this.logout(); // Token 无效，跳转到登录页面
          }
          throw new Error(`HTTP 错误! 状态码: ${response.status}`);
        }

        const user = await response.json();
        this.isAdmin = user.is_admin; // 假设后端返回的用户信息中包含 is_admin 字段
      } catch (error) {
        console.error('检查管理员状态失败', error);
      }
    },
    goToAdminPage() {
      this.$router.push('/admin'); // 跳转到管理员页面
    },
    newChat() {
      // 开启新对话的逻辑
      this.messages = [];
      this.chatHistory.push({
        id: Date.now(),
        title: `对话${this.chatHistory.length + 1}`,
        messages: [],
      });
      this.activeChatId = this.chatHistory[this.chatHistory.length - 1].id;
    },
    openSettings() {
      this.$router.push('/settings'); // 跳转到设置页面
    },
    logout() {
      // 退出登录的逻辑
      localStorage.removeItem('token');
      this.$router.push('/login');
    },
    sendMessage() {
      // 发送消息的逻辑
      if (this.message.trim()) {
        this.messages.push({ text: this.message, sender: 'user' });
        this.message = '';
      }
    },
    switchChat(chat) {
      // 切换对话的逻辑
      this.activeChatId = chat.id; // 设置当前选中的对话 ID
      this.messages = chat.messages || []; // 加载该对话的消息
    },
  },
  mounted() {
    this.checkAdminStatus(); // 组件加载时检查管理员状态
  },
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