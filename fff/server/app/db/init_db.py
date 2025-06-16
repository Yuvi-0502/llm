from sqlalchemy.orm import Session
from ..models.base import Base
from ..models.user import User, UserRole
from ..models.external_api import ExternalAPI
from ..core.config import settings
from .session import engine
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def init_db() -> None:
    # Create tables
    Base.metadata.create_all(bind=engine)

def create_initial_data(db: Session) -> None:
    # Create admin user if not exists
    admin = db.query(User).filter(User.email == "admin@example.com").first()
    if not admin:
        admin = User(
            username="admin",
            email="admin@example.com",
            hashed_password=pwd_context.hash("admin123"),
            role=UserRole.ADMIN
        )
        db.add(admin)
    
    # Create default external API configurations
    apis = [
        {
            "name": "News API",
            "base_url": "https://newsapi.org/v2",
            "api_key": settings.NEWS_API_KEY,
            "description": "News API for headlines and articles"
        },
        {
            "name": "The News API",
            "base_url": "https://api.thenewsapi.com/v1",
            "api_key": settings.THENEWS_API_KEY,
            "description": "The News API for headlines and articles"
        }
    ]
    
    for api_data in apis:
        api = db.query(ExternalAPI).filter(ExternalAPI.name == api_data["name"]).first()
        if not api:
            api = ExternalAPI(**api_data)
            db.add(api)
    
    db.commit()

if __name__ == "__main__":
    init_db()
    from .session import SessionLocal
    db = SessionLocal()
    create_initial_data(db)
    db.close() 