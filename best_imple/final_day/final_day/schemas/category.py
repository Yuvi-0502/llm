from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class CategoryResponse(CategoryBase):
    category_id: int
    created_at: datetime 