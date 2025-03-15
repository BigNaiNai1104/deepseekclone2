from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .database import SessionLocal, get_db
from . import models, crud, schemas

app = FastAPI()

# 配置 CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",  # 允许 Vite 开发服务器
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 根路由
@app.get("/")
def read_root():
    return {"message": "Welcome to DeepSeek Clone API"}

# 用户注册
@app.post("/api/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

# 用户登录
@app.post("/api/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    access_token = crud.verify_user(db=db, user=user)
    if not access_token:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"access_token": access_token, "token_type": "bearer"}

# 获取当前用户信息
@app.get("/api/me", response_model=schemas.User)
def get_current_user(db: Session = Depends(get_db), token: str = Depends(crud.oauth2_scheme)):
    user = crud.get_current_user(db, token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

# 定义聊天请求和响应模型
class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None

class ChatResponse(BaseModel):
    reply: str
    session_id: str

# 添加聊天路由
@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    # 模拟回复逻辑
    return {
        "reply": f"已收到你的消息：'{request.message}'（这是模拟回复）",
        "session_id": request.session_id or "new-session-id"
    }