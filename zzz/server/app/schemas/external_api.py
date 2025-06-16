from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class ExternalAPIBase(BaseModel):
    name: str
    base_url: HttpUrl
    api_key: str
    description: Optional[str] = None

class ExternalAPICreate(ExternalAPIBase):
    pass

class ExternalAPIUpdate(BaseModel):
    name: Optional[str] = None
    base_url: Optional[HttpUrl] = None
    api_key: Optional[str] = None
    is_active: Optional[bool] = None
    description: Optional[str] = None

class ExternalAPIInDB(ExternalAPIBase):
    id: int
    is_active: bool
    last_accessed: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ExternalAPI(ExternalAPIInDB):
    pass 