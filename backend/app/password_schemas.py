from pydantic import BaseModel

class PasswordChange(BaseModel):
    username: str
    old_password: str
    new_password: str