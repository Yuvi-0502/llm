from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    name: Optional[str] = None


class CategoryInDBBase(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class CategoryResponse(CategoryInDBBase):
    pass


class CategoryInDB(CategoryInDBBase):
    pass 