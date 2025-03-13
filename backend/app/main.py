# main.py
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from typing import Dict, List
import uuid
import time
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# --- 数据模型定义 ---
class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None  # 会话ID用于持续对话


class ChatResponse(BaseModel):
    reply: str
    session_id: str
    timestamp: int


# --- 业务逻辑类 ---
class ChatEngine:
    def __init__(self):
        # 使用字典模拟对话历史存储（生产环境请替换为数据库）
        self.sessions: Dict[str, List[dict]] = {}

    async def process_message(self, message: str, session_id: str | None) -> dict:
        """
        处理消息的核心逻辑
        """
        # 创建新会话（如果不存在）
        if not session_id or session_id not in self.sessions:
            session_id = str(uuid.uuid4())
            self.sessions[session_id] = [
                {"role": "system", "content": "你是一个乐于助人的智能助手"}
            ]

        # 添加用户消息到历史
        self.sessions[session_id].append({"role": "user", "content": message})

        try:
            # 🚀 此处替换为实际AI调用逻辑（示例为模拟回复）
            # 真实场景可接入 OpenAI/HuggingFace 等API
            ai_response = f"已收到你的消息：'{message}'（这是模拟回复）"

            # 添加助手回复到历史
            self.sessions[session_id].append({"role": "assistant", "content": ai_response})

            return {
                "reply": ai_response,
                "session_id": session_id,
                "timestamp": int(time.time())
            }

        except Exception as e:
            logger.error(f"AI处理失败: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="AI服务暂时不可用"
            )


# --- FastAPI 初始化 ---
app = FastAPI(title="智能聊天API")
chat_engine = ChatEngine()

# 配置CORS（开发用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 简单API密钥验证（可选）
api_key_header = APIKeyHeader(name="X-API-Key")
VALID_API_KEYS = {"your-secret-key"}  # 生产环境应从环境变量读取


async def validate_api_key(api_key: str = Depends(api_key_header)):
    if api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的API密钥"
        )
    return api_key


# --- API端点 ---
@app.post("/api/chat",
          response_model=ChatResponse,
          dependencies=[Depends(validate_api_key)])  # 启用身份验证
async def chat_endpoint(request: ChatRequest):
    """
    处理聊天消息，支持连续对话
    """
    try:
        response = await chat_engine.process_message(
            message=request.message,
            session_id=request.session_id
        )
        return response

    except Exception as e:
        logger.error(f"处理请求失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="服务器内部错误"
        )


# --- 健康检查端点 ---
@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": int(time.time())}