from dataclasses import dataclass

@dataclass
class ExternalServer:
    id: int
    name: str
    api_key: str
    base_url: str
    is_active: bool 