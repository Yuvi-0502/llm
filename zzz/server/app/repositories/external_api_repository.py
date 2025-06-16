from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.external_api import ExternalAPI
from app.repositories.base_repository import BaseRepository

class ExternalAPIRepository(BaseRepository[ExternalAPI]):
    """Repository for external API data access."""
    
    def __init__(self, db: Session):
        super().__init__(db, ExternalAPI)
        
    def get_by_name(self, name: str) -> Optional[ExternalAPI]:
        """Get external API by name."""
        return self.db.query(ExternalAPI).filter(ExternalAPI.name == name).first()
        
    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None
    ) -> List[ExternalAPI]:
        """Get all external APIs with optional filtering."""
        query = self.db.query(ExternalAPI)
        
        if is_active is not None:
            query = query.filter(ExternalAPI.is_active == is_active)
            
        return query.offset(skip).limit(limit).all()
        
    def create(self, api: ExternalAPI) -> ExternalAPI:
        """Create a new external API."""
        self.db.add(api)
        self.db.commit()
        self.db.refresh(api)
        return api
        
    def update(self, api_id: int, api: ExternalAPI) -> Optional[ExternalAPI]:
        """Update an existing external API."""
        db_api = self.get(api_id)
        if not db_api:
            return None
            
        for key, value in api.__dict__.items():
            if key != '_sa_instance_state':
                setattr(db_api, key, value)
                
        self.db.commit()
        self.db.refresh(db_api)
        return db_api
        
    def delete(self, api_id: int) -> bool:
        """Delete an external API."""
        api = self.get(api_id)
        if not api:
            return False
            
        self.db.delete(api)
        self.db.commit()
        return True
        
    def get_active_apis(self) -> List[ExternalAPI]:
        """Get all active external APIs."""
        return self.db.query(ExternalAPI).filter(ExternalAPI.is_active == True).all()
        
    def get_apis_accessed_after(self, date: datetime) -> List[ExternalAPI]:
        """Get APIs accessed after a specific date."""
        return self.db.query(ExternalAPI).filter(ExternalAPI.last_accessed >= date).all()
        
    def update_last_accessed(self, api_id: int) -> Optional[ExternalAPI]:
        """Update the last accessed timestamp for an API."""
        api = self.get(api_id)
        if not api:
            return None
            
        api.last_accessed = datetime.utcnow()
        self.db.commit()
        self.db.refresh(api)
        return api 