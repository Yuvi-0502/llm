from sqlalchemy.orm import Session
from app.models.user_article_feedback import UserArticleFeedback
from app.schemas.user_article_feedback import UserArticleFeedbackCreate

class UserArticleFeedbackRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, user_id: int, article_id: int):
        return self.db.query(UserArticleFeedback).filter(
            UserArticleFeedback.user_id == user_id,
            UserArticleFeedback.article_id == article_id
        ).first()

    def create(self, feedback: UserArticleFeedbackCreate):
        db_feedback = UserArticleFeedback(**feedback.dict())
        self.db.add(db_feedback)
        self.db.commit()
        self.db.refresh(db_feedback)
        return db_feedback

    def update(self, user_id: int, article_id: int, feedback: str):
        db_feedback = self.get(user_id, article_id)
        if db_feedback:
            db_feedback.feedback = feedback
            self.db.commit()
        return db_feedback 