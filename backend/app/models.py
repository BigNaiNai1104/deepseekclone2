from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import bcrypt
import uuid
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)  # 为 username 字段指定长度 50
    password_hash = Column(String(128))  # 密码字段保持原样
    created_at = Column(DateTime, default=datetime.utcnow)
    sessions = relationship("ChatSession", back_populates="owner")

    def set_password(self, password: str):
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        self.password_hash = hashed.hex()  # 保持密码哈希

    def verify_password(self, password: str) -> bool:
        try:
            stored_hash = bytes.fromhex(self.password_hash)  # 将密码哈希存储为字节
            return bcrypt.checkpw(password.encode(), stored_hash)
        except ValueError:
            return False


class ChatSession(Base):
    __tablename__ = "chat_sessions"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))  # UUID 长度 36
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    owner = relationship("User", back_populates="sessions")
    messages = relationship("ChatMessage", back_populates="session")


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True)
    session_id = Column(String(36), ForeignKey("chat_sessions.id"))
    role = Column(String(20))  # system/user/assistant
    content = Column(String(255))  # 为 content 字段指定最大长度 255
    timestamp = Column(DateTime, default=datetime.utcnow)
    session = relationship("ChatSession", back_populates="messages")
