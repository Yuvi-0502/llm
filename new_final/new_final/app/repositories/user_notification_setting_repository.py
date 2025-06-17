from sqlalchemy.orm import Session
from app.models.user_notification_setting import UserNotificationSetting
from app.schemas.user_notification_setting import UserNotificationSettingCreate

class UserNotificationSettingRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, setting_id: int):
        return self.db.query(UserNotificationSetting).filter(UserNotificationSetting.setting_id == setting_id).first()

    def get_by_user(self, user_id: int):
        return self.db.query(UserNotificationSetting).filter(UserNotificationSetting.user_id == user_id).all()

    def create(self, setting: UserNotificationSettingCreate):
        db_setting = UserNotificationSetting(**setting.dict())
        self.db.add(db_setting)
        self.db.commit()
        self.db.refresh(db_setting)
        return db_setting 