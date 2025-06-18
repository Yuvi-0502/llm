from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ExternalServerBase(BaseModel):
    server_name: str
    api_key: str
    base_url: str

class ExternalServerCreate(ExternalServerBase):
    pass

class ExternalServerUpdate(BaseModel):
    server_name: Optional[str] = None
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    is_active: Optional[bool] = None

class ExternalServerResponse(ExternalServerBase):
    server_id: int
    is_active: bool
    last_accessed: datetime
    created_at: datetime

    class Config:
        from_attributes = True