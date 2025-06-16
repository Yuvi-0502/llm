from sqlalchemy import Column, String, Boolean, DateTime
from .base import BaseModel

class ExternalAPI(BaseModel):
    __tablename__ = "external_apis"

    name = Column(String(100), nullable=False)
    base_url = Column(String(500), nullable=False)
    api_key = Column(String(200), nullable=False)
    is_active = Column(Boolean, default=True)
    last_accessed = Column(DateTime)
    description = Column(String(500)) 