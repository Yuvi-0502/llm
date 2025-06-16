from typing import Generator
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.repositories.article_repository import ArticleRepository
from app.repositories.user_repository import UserRepository
from app.repositories.external_api_repository import ExternalAPIRepository
from app.services.article import ArticleService
from app.services.user import UserService
from app.services.external_api import ExternalAPIService
from app.services.categorization import ArticleCategorizer

class Container:
    """Dependency injection container."""
    
    def __init__(self):
        self._db = SessionLocal()
        self._article_repository = ArticleRepository(self._db)
        self._user_repository = UserRepository(self._db)
        self._external_api_repository = ExternalAPIRepository(self._db)
        self._categorizer = ArticleCategorizer()
        
        self._article_service = ArticleService(
            repository=self._article_repository,
            categorizer=self._categorizer
        )
        self._user_service = UserService(repository=self._user_repository)
        self._external_api_service = ExternalAPIService(
            repository=self._external_api_repository
        )
        
    @property
    def db(self) -> Session:
        return self._db
        
    @property
    def article_service(self) -> ArticleService:
        return self._article_service
        
    @property
    def user_service(self) -> UserService:
        return self._user_service
        
    @property
    def external_api_service(self) -> ExternalAPIService:
        return self._external_api_service
        
    def get_db(self) -> Generator[Session, None, None]:
        try:
            yield self._db
        finally:
            self._db.close()
            
    def cleanup(self):
        """Cleanup resources."""
        self._db.close()

# Global container instance
container = Container()

def get_container() -> Container:
    """Get the global container instance."""
    return container 