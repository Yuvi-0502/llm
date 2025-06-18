from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    user_id: int
    user_name: str
    email: str
    password: str
    role: Optional[str]
    age: int

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    city: Optional[str] = None
    age: Optional[int] = None

class UserCreate(BaseModel):
    user_name: str
    email: str
    password: str
    role: Optional[str]
    age: int