from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional, Dict
from . import schemas

# 密钥和算法
SECRET_KEY = "mysecretkey"  # 应该从环境变量加载
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# 创建访问令牌
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建访问令牌
    :param data: 包含用户数据的字典
    :param expires_delta: 令牌过期时间，默认为30分钟
    :return: 编码后的JWT令牌
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # 生成 JWT 令牌
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 解析访问令牌
def verify_token(token: str) -> Optional[Dict]:
    """
    解析访问令牌
    :param token: JWT令牌
    :return: 解码后的payload，如果验证失败返回 None
    """
    try:
        # 解码JWT令牌
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # 返回有效负载（payload）
        return payload
    except JWTError as e:
        # 可以记录更详细的错误日志，以便调试
        print(f"JWTError: {e}")
        return None
    except Exception as e:
        # 捕获任何其他错误，并返回None
        print(f"Token 验证失败: {e}")
        return None
