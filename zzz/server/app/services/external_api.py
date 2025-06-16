from typing import List, Optional, Dict, Any
from datetime import datetime
from app.models.external_api import ExternalAPI
from app.dto.external_api import ExternalAPICreateDTO, ExternalAPIUpdateDTO
from app.repositories.external_api_repository import ExternalAPIRepository
from app.core.api_boundary import APIBoundary, RateLimitConfig, with_api_boundary
import requests

class ExternalAPIService:
    """Service for external API business logic."""
    
    def __init__(self, repository: ExternalAPIRepository):
        self.repository = repository
        self.boundary = APIBoundary(
            rate_limit=RateLimitConfig(
                requests_per_minute=60,
                requests_per_hour=1000,
                requests_per_day=10000
            )
        )

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

    def create_api(self, api: ExternalAPICreateDTO) -> ExternalAPI:
        if not self.boundary.validate_api_key(api.api_key):
            raise ValueError("Invalid API key format")
            
        db_api = ExternalAPI(
            name=api.name,
            base_url=api.base_url,
            api_key=api.api_key,
            description=api.description,
            is_active=True,
            last_accessed=datetime.utcnow()
        )
        return self.repository.create(db_api)

    def update_api(self, api_id: int, api: ExternalAPIUpdateDTO) -> Optional[ExternalAPI]:
        db_api = self.repository.get(api_id)
        if not db_api:
            return None

        if api.api_key and not self.boundary.validate_api_key(api.api_key):
            raise ValueError("Invalid API key format")

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
        
    @with_api_boundary
    async def make_api_request(
        self,
        api_id: int,
        endpoint: str,
        method: str = "GET",
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make a request to an external API with boundary controls."""
        api = self.get_api(api_id)
        if not api:
            raise ValueError("API not found")
            
        if not api.is_active:
            raise ValueError("API is not active")
            
        # Check API health
        health_status = self.boundary.check_api_health(api_id, api.base_url)
        if not health_status.is_healthy:
            raise ValueError(f"API is unhealthy: {health_status.last_error}")
            
        # Validate request data
        if data and not self.boundary.validate_request(data):
            raise ValueError("Invalid request data")
            
        # Make the request
        url = f"{api.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        headers = {"Authorization": f"Bearer {api.api_key}"}
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=data,
                timeout=10
            )
            response.raise_for_status()
            
            # Validate response
            response_data = response.json()
            if not self.boundary.validate_response(response_data):
                raise ValueError("Invalid response data")
                
            # Update last accessed
            self.update_last_accessed(api_id)
            
            return response_data
            
        except requests.exceptions.RequestException as e:
            raise ValueError(f"API request failed: {str(e)}")
            
    def get_api_stats(self) -> Dict[str, Any]:
        """Get statistics for all external APIs."""
        apis = self.get_apis()
        stats = {
            "total_apis": len(apis),
            "active_apis": len([api for api in apis if api.is_active]),
            "health_status": {}
        }
        
        for api in apis:
            health = self.boundary.check_api_health(api.id, api.base_url)
            stats["health_status"][api.name] = {
                "is_healthy": health.is_healthy,
                "response_time": health.response_time,
                "error_count": health.error_count,
                "last_error": health.last_error
            }
            
        return stats 