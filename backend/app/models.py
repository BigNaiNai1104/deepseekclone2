# --------------- app/models.py ---------------
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
import bcrypt
import uuid
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(60))
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    sessions = relationship("ChatSession", back_populates="owner")

    def set_password(self, password: str):
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        self.password = hashed.hex()

    def verify_password(self, password: str) -> bool:
        try:
            stored_hash = bytes.fromhex(self.password)
            return bcrypt.checkpw(password.encode(), stored_hash)
        except ValueError:
            return False

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    owner = relationship("User", back_populates="sessions")
    messages = relationship("ChatMessage", back_populates="session")

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True)
    session_id = Column(String(36), ForeignKey("chat_sessions.id"))
    role = Column(String(20))  # system/user/assistant
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    session = relationship("ChatSession", back_populates="messages")