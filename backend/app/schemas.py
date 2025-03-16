from pydantic import BaseModel

# 用户注册请求模型
class UserCreate(BaseModel):
    username: str
    password: str

# 用户登录请求模型
class UserLogin(BaseModel):
    username: str
    password: str

# 用户响应模型
class User(BaseModel):
    id: int
    username: str
    is_admin: bool

    class Config:
        from_attributes = True  # 允许从 ORM 模型转换为 Pydantic 模型

# 聊天请求模型
class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None

# 聊天响应模型
class ChatResponse(BaseModel):
    reply: str
    session_id: str
    history: list

# 修改密码请求模型
class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

# 用户设置请求模型
class SettingsRequest(BaseModel):
    username: str | None = None
    password: str | None = None