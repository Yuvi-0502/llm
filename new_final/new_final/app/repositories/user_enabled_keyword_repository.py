from sqlalchemy.orm import Session
from app.models.user_enabled_keyword import UserEnabledKeyword
from app.schemas.user_enabled_keyword import UserEnabledKeywordCreate

class UserEnabledKeywordRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, id: int):
        return self.db.query(UserEnabledKeyword).filter(UserEnabledKeyword.id == id).first()

    def get_by_user(self, user_id: int):
        return self.db.query(UserEnabledKeyword).filter(UserEnabledKeyword.user_id == user_id).all()

    def create(self, user_enabled_keyword: UserEnabledKeywordCreate):
        db_uek = UserEnabledKeyword(**user_enabled_keyword.dict())
        self.db.add(db_uek)
        self.db.commit()
        self.db.refresh(db_uek)
        return db_uek 