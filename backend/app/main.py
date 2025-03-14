from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 安全优化的CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发环境允许所有源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=[       # 明确允许的请求头
        "Authorization",  # JWT令牌头
        "Content-Type"    # 内容类型头
    ]
)

@app.get("/")
def read_root():
    return {"message": "Welcome to DeepSeek Clone API"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/register", response_model=schemas.UserCreate)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = crud.create_user(db=db, user=user)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error during registration: " + str(e))

@app.post("/api/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    access_token = crud.verify_user(db=db, user=user)
    if not access_token:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"access_token": access_token, "token_type": "bearer"}