from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: int
    username: str
    email: str
    is_admin: bool
    token: Optional[str] = None 