from pydantic import BaseModel
from datetime import datetime

# Token 响应模型
class Token(BaseModel):
    access_token: str
    token_type: str

# Token 数据模型
class TokenData(BaseModel):
    username: str | None = None

# 用户基础模型
class UserBase(BaseModel):
    username: str

# 用户创建模型
class UserCreate(UserBase):
    password: str

# 用户响应模型
class User(UserBase):
    id: int
    is_admin: bool = False

    class Config:
        from_attributes = True  # 替换 orm_mode = True

# 消息基础模型
class MessageBase(BaseModel):
    content: str

# 消息创建模型
class MessageCreate(MessageBase):
    sender_id: int
    receiver_id: int

# 消息响应模型
class Message(MessageBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True  # 替换 orm_mode = True