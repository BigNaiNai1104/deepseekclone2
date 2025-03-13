from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime
import bcrypt

# 用户模型
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    # 用户与聊天记录的关系
    chat_history = relationship("ChatHistory", back_populates="owner")

    def set_password(self, password: str):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))


# 示例模型：聊天历史记录
class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # 设置与 User 模型的关系
    owner = relationship("User", back_populates="chat_history")
