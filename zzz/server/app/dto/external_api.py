from typing import Optional
from pydantic import BaseModel, HttpUrl, constr
from datetime import datetime

# Request DTOs
class ExternalAPICreateDTO(BaseModel):
    name: constr(min_length=1, max_length=100)
    base_url: HttpUrl
    api_key: constr(min_length=1)
    description: Optional[constr(max_length=500)] = None

class ExternalAPIUpdateDTO(BaseModel):
    name: Optional[constr(min_length=1, max_length=100)] = None
    base_url: Optional[HttpUrl] = None
    api_key: Optional[constr(min_length=1)] = None
    description: Optional[constr(max_length=500)] = None
    is_active: Optional[bool] = None

# Response DTOs
class ExternalAPIResponseDTO(BaseModel):
    id: int
    name: str
    base_url: str
    api_key: str
    description: Optional[str]
    is_active: bool
    last_accessed: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ExternalAPIListResponseDTO(BaseModel):
    apis: list[ExternalAPIResponseDTO]
    total: int
    page: int
    size: int

class ExternalAPIStatsDTO(BaseModel):
    total_apis: int
    active_apis: int
    last_fetch_time: Optional[datetime]
    average_response_time: Optional[float]
    success_rate: Optional[float] 