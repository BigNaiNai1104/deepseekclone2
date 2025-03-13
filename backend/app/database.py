from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from fastapi import FastAPI
import logging

# 加载 .env 文件
load_dotenv()

# 获取数据库连接配置
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "mysql+mysqlconnector://root:021104@localhost/deepseek2")

# 创建数据库引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # 如果是 MySQL，可以移除此参数
)

# 创建会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 基类
Base = declarative_base()

# FastAPI 应用
app = FastAPI()

# 数据库会话依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 配置日志
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# 调试：确认数据库连接
@app.on_event("startup")
async def startup_db():
    try:
        with engine.connect() as connection:
            logger.info("Database connected successfully!")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
