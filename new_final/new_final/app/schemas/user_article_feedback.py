from pydantic import BaseModel

class UserArticleFeedbackBase(BaseModel):
    user_id: int
    article_id: int
    feedback: str

class UserArticleFeedbackCreate(UserArticleFeedbackBase):
    pass

class UserArticleFeedbackOut(UserArticleFeedbackBase):
    class Config:
        orm_mode = True 