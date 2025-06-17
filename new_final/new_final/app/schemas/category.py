from pydantic import BaseModel

class CategoryBase(BaseModel):
    category_name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    category_id: int

    class Config:
        orm_mode = True 