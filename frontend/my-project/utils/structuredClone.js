// utils/structuredClone.js

// 如果 Node.js 版本不支持 structuredClone，可以使用以下代码模拟深拷贝
if (typeof structuredClone === 'undefined') {
    global.structuredClone = function(obj) {
      return JSON.parse(JSON.stringify(obj));
    };
  }
  