from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class ExternalServerBase(BaseModel):
    name: str
    base_url: str
    is_active: bool = True


class ExternalServerCreate(ExternalServerBase):
    api_key: str


class ExternalServerUpdate(BaseModel):
    api_key: Optional[str] = None
    is_active: Optional[bool] = None


class ExternalServerInDBBase(ExternalServerBase):
    id: int
    last_accessed: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class ExternalServerResponse(ExternalServerInDBBase):
    pass


class ExternalServerInDB(ExternalServerInDBBase):
    api_key: str 