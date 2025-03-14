from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from fastapi.security import OAuth2PasswordBearer

# 密码加密工具
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 密钥用于 JWT 签名（注意生产环境中应该从环境变量中读取）
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2密码认证的Bearer Token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

# 验证用户并生成JWT
def verify_user(db: Session, user: schemas.UserLogin):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user and pwd_context.verify(user.password, db_user.password_hash):  # 修改为 password_hash
        # 生成 JWT Token
        access_token = create_access_token(data={"sub": db_user.username})
        return access_token
    return None

# 创建用户
def create_user(db: Session, user: schemas.UserCreate):
    # 密码加密
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, password_hash=hashed_password)  # 使用 password_hash
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 创建 JWT 令牌
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
