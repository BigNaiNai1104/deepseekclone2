from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, get_db
from app import models, crud, schemas
import os

# 初始化数据库表
models.Base.metadata.create_all(bind=engine)

# 创建 FastAPI 实例
app = FastAPI()

# 配置 CORS 跨域
origins = [
    "http://localhost",
    "http://localhost:8000",  # 修改为新的端口号
    "http://127.0.0.1:8000",  # 修改为新的端口号
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


# 用户注册 API
@app.post("/api/register", response_model=schemas.UserCreate)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        # 检查用户是否已存在
        db_user = crud.get_user_by_username(db, username=user.username)
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")

        # 创建用户
        db_user = crud.create_user(db=db, user=user)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error during registration: {str(e)}")


# 用户登录 API
@app.post("/api/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    # 验证用户
    access_token = crud.verify_user(db=db, user=user)
    if not access_token:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # 返回访问令牌
    return {"access_token": access_token, "token_type": "bearer"}


# 获取当前用户信息
@app.get("/api/me", response_model=schemas.User)
def get_current_user(db: Session = Depends(get_db), token: str = Depends(crud.oauth2_scheme)):
    # 验证令牌并获取用户信息
    user = crud.get_current_user(db, token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user


# 数据库会话管理
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()