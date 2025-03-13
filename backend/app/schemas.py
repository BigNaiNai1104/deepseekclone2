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
