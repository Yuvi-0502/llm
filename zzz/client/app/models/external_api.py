from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ExternalAPI:
    id: int
    name: str
    base_url: str
    api_key: str
    is_active: bool
    last_accessed: Optional[datetime]
    description: Optional[str]

@dataclass
class ExternalAPICreate:
    name: str
    base_url: str
    api_key: str
    description: Optional[str] = None

@dataclass
class ExternalAPIUpdate:
    name: Optional[str] = None
    base_url: Optional[str] = None
    api_key: Optional[str] = None
    is_active: Optional[bool] = None
    description: Optional[str] = None 