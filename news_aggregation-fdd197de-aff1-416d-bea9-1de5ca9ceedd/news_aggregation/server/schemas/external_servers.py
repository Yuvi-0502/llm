from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ExternalServerUpdate(BaseModel):
    api_key: str