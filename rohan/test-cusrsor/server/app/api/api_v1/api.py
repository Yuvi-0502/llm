from fastapi import APIRouter
from app.api.api_v1.endpoints import (
    auth,
    users,
    articles,
    categories,
    external_servers,
    notifications
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(articles.router, prefix="/articles", tags=["articles"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(external_servers.router, prefix="/external-servers", tags=["external-servers"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"]) 