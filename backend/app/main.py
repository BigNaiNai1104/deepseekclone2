from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import schemas, crud
from .database import get_db
from .services.chat_service import ChatService
import time

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

app = FastAPI(title="DeepSeek API")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 依赖项
async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    return crud.get_current_user(db, token)

async def require_admin(user = Depends(get_current_user)):
    crud.require_admin(user)
    return user

# 路由
@app.post("/api/register")
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.post("/api/login")
async def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    return crud.authenticate_user(db, user)

@app.post("/api/chat")
async def chat_endpoint(
    request: schemas.ChatRequest,
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = ChatService(db)
    return service.process_message(user.id, request.message, request.session_id)

@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": int(time.time())}