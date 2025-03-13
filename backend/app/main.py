from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from . import crud, models, schemas, auth, database

# 初始化 FastAPI 应用
app = FastAPI()

# 允许跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有请求头
)

# 创建数据库会话
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 登录接口
@app.post("/users/login")
async def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.verify_user(db, user)
    if not db_user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    access_token = auth.create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# 注册接口
@app.post("/users/register")
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db, user)
    return {"message": "注册成功"}

# 创建所有表
from .database import Base, engine
Base.metadata.create_all(bind=engine)

# 根路径
@app.get("/")
async def root():
    return {"message": "Hello, World!"}
