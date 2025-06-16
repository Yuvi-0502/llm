from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List
import schedule
import time
import threading
import asyncio

from app.core.config import settings
from app.core.security import create_access_token, verify_token
from app.db.base import get_db, engine, Base
from app.models import models
from app.schemas import schemas
from app.services.news_service import NewsService
from app.services.user_service import UserService

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login")

# Dependency to get current user
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    username = verify_token(token)
    if username is None:
        raise credentials_exception
    
    user_service = UserService(db)
    user = user_service.get_user_by_username(username)
    if user is None:
        raise credentials_exception
    return user

# Dependency to get current active user
async def get_current_active_user(
    current_user: models.User = Depends(get_current_user)
) -> models.User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Background task for news aggregation
async def aggregate_news_periodically():
    while True:
        db = next(get_db())
        news_service = NewsService(db)
        await news_service.aggregate_news()
        await asyncio.sleep(4 * 60 * 60)  # 4 hours

@app.on_event("startup")
async def startup_event():
    # Start background task for news aggregation
    asyncio.create_task(aggregate_news_periodically())

# Authentication routes
@app.post(f"{settings.API_V1_STR}/login", response_model=schemas.Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user_service = UserService(db)
    user = user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post(f"{settings.API_V1_STR}/signup", response_model=schemas.UserInDB)
async def signup(
    user_data: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    user_service = UserService(db)
    user = user_service.create_user(user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )
    return user

# News routes
@app.get(f"{settings.API_V1_STR}/news/category/{{category}}", response_model=List[schemas.NewsArticleInDB])
async def get_news_by_category(
    category: str,
    limit: int = 10,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    news_service = NewsService(db)
    return news_service.get_news_by_category(category, limit)

@app.get(f"{settings.API_V1_STR}/news/search", response_model=List[schemas.NewsArticleInDB])
async def search_news(
    query: str,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    news_service = NewsService(db)
    return news_service.search_news(query)

@app.post(f"{settings.API_V1_STR}/news/save/{{article_id}}")
async def save_article(
    article_id: int,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    news_service = NewsService(db)
    if news_service.save_article_for_user(current_user.id, article_id):
        return {"message": "Article saved successfully"}
    raise HTTPException(status_code=404, detail="Article not found")

@app.get(f"{settings.API_V1_STR}/news/saved", response_model=List[schemas.NewsArticleInDB])
async def get_saved_articles(
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    news_service = NewsService(db)
    return news_service.get_saved_articles(current_user.id)

# Notification routes
@app.get(f"{settings.API_V1_STR}/notifications/preferences", response_model=List[schemas.NotificationPreferenceInDB])
async def get_notification_preferences(
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    user_service = UserService(db)
    return user_service.get_notification_preferences(current_user.id)

@app.put(f"{settings.API_V1_STR}/notifications/preferences/{{category}}")
async def update_notification_preference(
    category: str,
    is_enabled: bool,
    keywords: str = None,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    user_service = UserService(db)
    if user_service.update_notification_preference(current_user.id, category, is_enabled, keywords):
        return {"message": "Notification preference updated successfully"}
    raise HTTPException(status_code=404, detail="Category not found")

# Admin routes
@app.get(f"{settings.API_V1_STR}/admin/servers", response_model=List[schemas.ExternalServerInDB])
async def get_external_servers(
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    return db.query(models.ExternalServer).all()

@app.post(f"{settings.API_V1_STR}/admin/servers", response_model=schemas.ExternalServerInDB)
async def create_external_server(
    server_data: schemas.ExternalServerCreate,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    server = models.ExternalServer(**server_data.dict())
    db.add(server)
    db.commit()
    db.refresh(server)
    return server

@app.put(f"{settings.API_V1_STR}/admin/servers/{{server_id}}", response_model=schemas.ExternalServerInDB)
async def update_external_server(
    server_id: int,
    server_data: schemas.ExternalServerUpdate,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    server = db.query(models.ExternalServer).get(server_id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    
    for key, value in server_data.dict(exclude_unset=True).items():
        setattr(server, key, value)
    
    db.commit()
    db.refresh(server)
    return server

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 