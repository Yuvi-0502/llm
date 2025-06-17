from pydantic import BaseModel

class ArticleCategoryMappingBase(BaseModel):
    category_id: int
    article_id: int

class ArticleCategoryMappingCreate(ArticleCategoryMappingBase):
    pass

class ArticleCategoryMappingOut(ArticleCategoryMappingBase):
    article_category_mapping_id: int

    class Config:
        orm_mode = True 