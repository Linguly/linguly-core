from pydantic import BaseModel
from typing import Optional


class LoginRequest(BaseModel):
    email: str
    password: str


class SignupRequest(BaseModel):
    email: str
    password: str
    name: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# UserInfo used in the Token
class UserInfo(BaseModel):
    user_id: Optional[str] = None  # user ID
    email: Optional[str] = None  # user email
    name: Optional[str] = None  # user name
