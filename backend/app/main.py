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

# 修改用户设置
@app.post("/api/settings")
def update_settings(
    request: schemas.SettingsRequest,
    db: Session = Depends(get_db),
    token: str = Depends(crud.oauth2_scheme)
):
    current_user = crud.get_current_user(db, token)
    if not current_user:
        raise HTTPException(status_code=401, detail="Invalid token")

    if request.username:
        current_user.username = request.username
    if request.password:
        current_user.password_hash = crud.get_password_hash(request.password)

    db.commit()
    return {"message": "设置更新成功"}

# 管理员专属功能：获取所有用户
@app.get("/api/admin/users", response_model=list[schemas.User])
def get_all_users(db: Session = Depends(get_db), token: str = Depends(crud.oauth2_scheme)):
    current_user = crud.get_current_user(db, token)
    if not current_user or not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")
    return crud.get_all_users(db)

# 管理员专属功能：提升用户为管理员
@app.post("/api/admin/promote")
def promote_user(username: str, db: Session = Depends(get_db), token: str = Depends(crud.oauth2_scheme)):
    current_user = crud.get_current_user(db, token)
    if not current_user or not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")
    return crud.promote_to_admin(db, username)

# 聊天功能
@app.post("/api/chat")
async def chat_endpoint(request: schemas.ChatRequest, db: Session = Depends(get_db)):
    # 模拟回复逻辑
    return {
        "reply": f"已收到你的消息：'{request.message}'（这是模拟回复）",
        "session_id": request.session_id or "new-session-id"
    }