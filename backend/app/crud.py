from sqlalchemy.orm import Session
from . import models, schemas
import bcrypt
from datetime import datetime, timedelta
import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException

# 密钥用于 JWT 签名
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2密码认证的Bearer Token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码是否正确"""
    try:
        # 将十六进制哈希值转换为字节
        stored_hash = bytes.fromhex(hashed_password)
        return bcrypt.checkpw(plain_password.encode(), stored_hash)
    except ValueError:
        return False

def get_password_hash(password: str) -> str:
    """生成密码的哈希值"""
    # 使用 bcrypt 生成哈希值，并转换为十六进制字符串存储
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed.hex()

def verify_user(db: Session, user: schemas.UserLogin):
    """验证用户并生成 JWT"""
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user and verify_password(user.password, db_user.password_hash):
        # 生成 JWT Token
        access_token = create_access_token(data={"sub": db_user.username})
        return access_token
    return None

def create_user(db: Session, user: schemas.UserCreate):
    """创建用户"""
    try:
        # 检查用户是否已存在
        db_user = db.query(models.User).filter(models.User.username == user.username).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")

        # 密码加密
        hashed_password = get_password_hash(user.password)
        db_user = models.User(username=user.username, password_hash=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    """创建 JWT 令牌"""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(db: Session, token: str):
    """获取当前用户"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            return None
        user = db.query(models.User).filter(models.User.username == username).first()
        return user
    except jwt.PyJWTError:
        return None

def get_all_users(db: Session):
    """获取所有用户"""
    return db.query(models.User).all()

def promote_to_admin(db: Session, username: str):
    """将用户提升为管理员"""
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if not db_user:
        return None
    db_user.is_admin = True
    db.commit()
    db.refresh(db_user)
    return db_user