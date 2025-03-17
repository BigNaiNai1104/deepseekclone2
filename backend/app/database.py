from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import logging

# 保留你的 MySQL 连接 URL
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:021104@localhost/deepseek2"

# 配置日志记录（可选，用于调试）
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# 创建数据库引擎（添加连接池配置）
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=QueuePool,  # 使用连接池
    pool_size=5,          # 连接池大小
    max_overflow=10,      # 最大溢出连接数
    pool_timeout=30,      # 连接超时时间（秒）
    pool_recycle=3600     # 连接回收时间（秒）
)

# 创建本地会话类
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 声明基类
Base = declarative_base()

# 测试数据库连接（可选）
if __name__ == "__main__":
    try:
        with engine.connect() as connection:
            print("MySQL 连接成功！")
    except Exception as e:
        print(f"MySQL 连接失败: {e}")