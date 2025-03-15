<template>
  <div class="app-container">
    <!-- 左侧边栏 -->
    <div class="sidebar">
      <div class="sidebar-header">
        <h2>对话历史</h2>
      </div>
      <div class="chat-list">
        <div
          v-for="(chat, index) in chatHistoryList"
          :key="index"
          class="chat-item"
          :class="{ active: activeChatIndex === index }"
          @click="switchChat(index)"
        >
          <span>{{ chat.title || `对话 ${index + 1}` }}</span>
          <el-button type="link" icon="el-icon-delete" @click.stop="deleteChat(index)"></el-button>
        </div>
      </div>

      <!-- 竖排按钮 -->
      <div class="sidebar-buttons">
        <el-button type="link" @click="newChat">
          <img :src="buttonIcons.newChat" alt="新建对话" class="button-icon" />
        </el-button>
        <el-button type="link" @click="resetChat">
          <img :src="buttonIcons.resetChat" alt="重置对话" class="button-icon" />
        </el-button>
        <el-button type="link" @click="exportChat">
          <img :src="buttonIcons.exportChat" alt="导出记录" class="button-icon" />
        </el-button>
        <el-button type="link" @click="openSettings">
          <img :src="buttonIcons.settings" alt="设置" class="button-icon" />
        </el-button>
      </div>
    </div>

    <!-- 右侧主内容 -->
    <div class="main-content">
      <!-- 消息区域 -->
      <div ref="messagesContainer" class="messages">
        <div 
          v-for="(msg, index) in activeChat.messages" 
          :key="index" 
          class="message" 
          :class="{ 'user-message': msg.role === 'user' }"
        >
          <!-- 助手头像 -->
          <div v-if="msg.role === 'assistant'" class="avatar">🤖</div>
          
          <!-- 消息气泡 -->
          <div class="bubble">
            <pre v-if="msg.isCode" class="code-block">{{ msg.content }}</pre>
            <p v-else>{{ msg.content }}</p>
            <span class="timestamp">{{ msg.time }}</span>
            <button class="copy-btn" @click="copyText(msg.content)">📋</button>
          </div>

          <!-- 用户头像 -->
          <div v-if="msg.role === 'user'" class="avatar">👤</div>
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="input-area">
        <el-input
          v-model="message"
          placeholder="请输入消息..."
          @keyup.enter="sendMessage"
          :disabled="isLoading"
          clearable
        ></el-input>
        <el-button 
          @click="sendMessage" 
          type="primary" 
          :disabled="isLoading"
        >
          {{ isLoading ? '发送中...' : '发送' }}
        </el-button>
      </div>

      <!-- 加载状态 -->
      <div v-if="isLoading" class="loading">
        <div class="dot-flashing"></div>
        <span>正在思考中...</span>
      </div>

      <!-- 设置弹窗 -->
      <el-dialog title="设置" :visible.sync="settingsVisible" width="30%">
        <el-form label-width="80px">
          <el-form-item label="API 密钥">
            <el-input v-model="apiKey" placeholder="请输入API密钥"></el-input>
          </el-form-item>
          <el-form-item label="主题">
            <el-select v-model="theme" placeholder="请选择主题">
              <el-option label="浅色" value="light"></el-option>
              <el-option label="深色" value="dark"></el-option>
            </el-select>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
          <el-button @click="settingsVisible = false">取消</el-button>
          <el-button type="primary" @click="saveSettings">保存</el-button>
        </span>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      message: '',
      isLoading: false,
      settingsVisible: false,
      apiKey: localStorage.getItem('api_key') || '',
      theme: localStorage.getItem('theme') || 'light',
      chatHistoryList: [
        {
          title: '默认对话',
          messages: [],
          sessionId: null
        }
      ],
      activeChatIndex: 0,
      // 图片路径
      buttonIcons: {
        newChat: new URL('./assets/new-chat.png', import.meta.url).href,
        resetChat: new URL('./assets/reset-chat.png', import.meta.url).href,
        exportChat: new URL('./assets/export-chat.png', import.meta.url).href,
        settings: new URL('./assets/settings.png', import.meta.url).href
      }
    }
  },
  computed: {
    activeChat() {
      return this.chatHistoryList[this.activeChatIndex]
    }
  },
  watch: {
    theme(newTheme) {
      document.body.className = newTheme + '-theme'
    }
  },
  mounted() {
    document.body.className = this.theme + '-theme'
  },
  methods: {
    async sendMessage() {
      if (this.message.trim() === '' || this.isLoading) return

      // 添加用户消息
      this.activeChat.messages.push({
        role: 'user',
        content: this.message,
        time: this.getCurrentTime()
      })

      this.isLoading = true
      const userMessage = this.message
      this.message = ''
      this.scrollToBottom()

      try {
        const response = await axios.post(
          'http://localhost:8000/api/chat',
          {
            message: userMessage,
            session_id: this.activeChat.sessionId
          },
          {
            headers: {
              'X-API-Key': this.apiKey
            }
          }
        )

        // 更新会话ID
        this.activeChat.sessionId = response.data.session_id
        localStorage.setItem('session_id', this.activeChat.sessionId)

        // 添加助手回复
        this.activeChat.messages.push({
          role: 'assistant',
          content: response.data.reply,
          time: this.getCurrentTime()
        })
      } catch (error) {
        this.$message.error('消息发送失败：' + (error.response ? error.response.data.detail : error.message))
      } finally {
        this.isLoading = false
        this.scrollToBottom()
      }
    },
    getCurrentTime() {
      return new Date().toLocaleTimeString()
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.messagesContainer
        if (container) {
          container.scrollTop = container.scrollHeight
        }
      })
    },
    resetChat() {
      this.activeChat.messages = []
      this.activeChat.sessionId = null
      localStorage.removeItem('session_id')
      this.$message.success('对话已重置')
    },
    exportChat() {
      const chatText = this.activeChat.messages.map(msg => `${msg.role}: ${msg.content}`).join('\n')
      const blob = new Blob([chatText], { type: 'text/plain' })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = 'chat_history.txt'
      link.click()
      URL.revokeObjectURL(url)
    },
    openSettings() {
      this.settingsVisible = true
    },
    saveSettings() {
      localStorage.setItem('api_key', this.apiKey)
      localStorage.setItem('theme', this.theme)
      this.settingsVisible = false
      this.$message.success('设置已保存')
    },
    copyText(text) {
      navigator.clipboard.writeText(text)
        .then(() => this.$message.success('已复制到剪贴板'))
        .catch(() => this.$message.error('复制失败'))
    },
    newChat() {
      this.chatHistoryList.push({
        title: `对话 ${this.chatHistoryList.length + 1}`,
        messages: [],
        sessionId: null
      })
      this.activeChatIndex = this.chatHistoryList.length - 1
    },
    switchChat(index) {
      this.activeChatIndex = index
    },
    deleteChat(index) {
      this.chatHistoryList.splice(index, 1)
      if (this.activeChatIndex >= index) {
        this.activeChatIndex = Math.max(0, this.activeChatIndex - 1)
      }
    }
  }
}
</script>

<style scoped>
/* 浅色主题 */
body.light-theme {
  --bg-color: #ffffff;
  --text-color: #333;
  --bubble-bg: #fff;
  --user-bubble-bg: #e3f2fd;
  --sidebar-bg: #f0f8ff; /* 淡蓝色 */
  --sidebar-border: #e0e0e0;
}

/* 深色主题 */
body.dark-theme {
  --bg-color: #1e1e1e;
  --text-color: #e0e0e0;
  --bubble-bg: #2d2d2d;
  --user-bubble-bg: #004080;
  --sidebar-bg: #1a3650; /* 深蓝色 */
  --sidebar-border: #333333;
}

.app-container {
  display: flex;
  height: 100vh;
  background: var(--bg-color);
  color: var(--text-color);
}

.sidebar {
  width: 250px;
  background: var(--sidebar-bg);
  border-right: 1px solid var(--sidebar-border);
  padding: 16px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  margin-bottom: 16px;
}

.chat-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.chat-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;
}

.chat-item:hover {
  background: rgba(0, 0, 0, 0.1);
}

.chat-item.active {
  background: var(--user-bubble-bg);
}

.sidebar-buttons {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 16px;
}

.button-icon {
  width: 24px;
  height: 24px;
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

.input-area {
  display: flex;
  gap: 12px;
  padding: 16px;
  background: var(--bg-color);
  border-top: 1px solid var(--sidebar-border);
}

.loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: var(--text-color);
  padding: 12px;
}

/* 其他样式保持不变 */
</style>