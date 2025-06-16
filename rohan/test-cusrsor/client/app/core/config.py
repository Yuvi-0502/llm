from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    PROJECT_NAME: str = "News Aggregator Client"
    VERSION: str = "1.0.0"
    API_URL: str = "http://localhost:8000/api/v1"
    
    class Config:
        case_sensitive = True
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings() 