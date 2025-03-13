from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException

# 验证用户
def verify_user(db: Session, user: schemas.UserLogin):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user and db_user.password == user.password:
        return db_user
    return None

# 创建用户
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
