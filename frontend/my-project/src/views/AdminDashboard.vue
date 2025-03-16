<template>
    <div class="admin-dashboard">
      <h1>管理员仪表盘</h1>
      <div class="admin-actions">
        <button @click="viewUsers">查看用户</button>
        <button @click="viewChats">查看对话</button>
        <button @click="logout">退出</button>
      </div>
      <div v-if="currentView === 'users'">
        <h2>用户列表</h2>
        <ul>
          <li v-for="user in users" :key="user.id">
            {{ user.name }} - {{ user.email }}
            <button @click="editUser(user)">编辑</button>
            <button @click="deleteUser(user)">删除</button>
          </li>
        </ul>
      </div>
      <div v-if="currentView === 'chats'">
        <h2>对话记录</h2>
        <ul>
          <li v-for="chat in chats" :key="chat.id">
            {{ chat.user }} - {{ chat.message }}
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'AdminDashboard',
    data() {
      return {
        currentView: 'users', // 当前视图：users 或 chats
        users: [
          { id: 1, name: '用户1', email: 'user1@example.com' },
          { id: 2, name: '用户2', email: 'user2@example.com' }
        ],
        chats: [
          { id: 1, user: '用户1', message: '你好，我有一个问题。' },
          { id: 2, user: '用户2', message: '如何重置密码？' }
        ]
      };
    },
    methods: {
      viewUsers() {
        this.currentView = 'users';
      },
      viewChats() {
        this.currentView = 'chats';
      },
      editUser(user) {
        alert(`编辑用户：${user.name}`);
        // 这里可以实现编辑用户的逻辑
      },
      deleteUser(user) {
        if (confirm(`确定删除用户 ${user.name} 吗？`)) {
          this.users = this.users.filter(u => u.id !== user.id);
        }
      },
      logout() {
        localStorage.removeItem('isAdmin');
        this.$router.push('/admin/login');
      }
    },
    beforeRouteEnter(to, from, next) {
      // 路由守卫：检查是否为管理员
      const isAdmin = localStorage.getItem('isAdmin') === 'true';
      if (isAdmin) {
        next();
      } else {
        next('/admin/login');
      }
    }
  };
  </script>
  
  <style scoped>
  .admin-dashboard {
    padding: 24px;
    background: #1e1e1e;
    color: #ffffff;
  }
  
  .admin-actions {
    display: flex;
    gap: 12px;
    margin-bottom: 24px;
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
  
  ul {
    list-style-type: none;
    padding: 0;
  }
  
  li {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;
  }
  </style>