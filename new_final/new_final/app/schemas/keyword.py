from pydantic import BaseModel

class KeywordBase(BaseModel):
    keyword_name: str

class KeywordCreate(KeywordBase):
    pass

class KeywordOut(KeywordBase):
    keyword_id: int

    class Config:
        orm_mode = True 