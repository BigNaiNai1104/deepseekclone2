from pydantic import BaseModel

# 用户登录验证模式
class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True

# 用户注册验证模式
class UserCreate(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True

# 响应模式：用于用户登录/注册后的响应
class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True
