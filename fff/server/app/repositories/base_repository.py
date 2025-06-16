from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional
from sqlalchemy.orm import Session

T = TypeVar('T')

class BaseRepository(Generic[T], ABC):
    """Base repository interface for database operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    @abstractmethod
    def get(self, id: int) -> Optional[T]:
        """Get an entity by ID."""
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all entities with pagination."""
        pass
    
    @abstractmethod
    def create(self, entity: T) -> T:
        """Create a new entity."""
        pass
    
    @abstractmethod
    def update(self, id: int, entity: T) -> Optional[T]:
        """Update an existing entity."""
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        """Delete an entity."""
        pass 