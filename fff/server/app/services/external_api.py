from typing import List, Optional
from datetime import datetime
from app.models.external_api import ExternalAPI
from app.schemas.external_api import ExternalAPICreate, ExternalAPIUpdate
from app.repositories.external_api_repository import ExternalAPIRepository

class ExternalAPIService:
    """Service for external API business logic."""
    
    def __init__(self, repository: ExternalAPIRepository):
        self.repository = repository

    def get_apis(
        self,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None
    ) -> List[ExternalAPI]:
        return self.repository.get_all(
            skip=skip,
            limit=limit,
            is_active=is_active
        )

    def get_api(self, api_id: int) -> Optional[ExternalAPI]:
        return self.repository.get(api_id)

    def get_api_by_name(self, name: str) -> Optional[ExternalAPI]:
        return self.repository.get_by_name(name)

    def create_api(self, api: ExternalAPICreate) -> ExternalAPI:
        db_api = ExternalAPI(
            name=api.name,
            base_url=api.base_url,
            api_key=api.api_key,
            description=api.description,
            is_active=True,
            last_accessed=datetime.utcnow()
        )
        return self.repository.create(db_api)

    def update_api(self, api_id: int, api: ExternalAPIUpdate) -> Optional[ExternalAPI]:
        db_api = self.repository.get(api_id)
        if not db_api:
            return None

        update_data = api.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_api, key, value)

        return self.repository.update(api_id, db_api)

    def delete_api(self, api_id: int) -> bool:
        return self.repository.delete(api_id)

    def get_active_apis(self) -> List[ExternalAPI]:
        return self.repository.get_active_apis()

    def get_apis_accessed_after(self, date: datetime) -> List[ExternalAPI]:
        return self.repository.get_apis_accessed_after(date)

    def update_last_accessed(self, api_id: int) -> Optional[ExternalAPI]:
        return self.repository.update_last_accessed(api_id) 