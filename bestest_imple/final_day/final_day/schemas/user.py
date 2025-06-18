from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    user_name: str
    email: EmailStr
    role: Optional[str] = "user"

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    user_id: int
    role: str
    created_at: datetime = datetime.now()

class UserLogin(BaseModel):
    email: EmailStr
    password: str

