from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.endpoints import auth, news, users
from app.db.base import Base
from app.db.session import engine
import asyncio
from app.services.news_service import NewsService
from app.db.session import SessionLocal
import schedule
import time
import threading

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(news.router, prefix=f"{settings.API_V1_STR}/news", tags=["news"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])

async def fetch_news():
    """
    Background task to fetch news from external APIs.
    """
    db = SessionLocal()
    try:
        news_service = NewsService(db)
        await news_service.process_and_store_news()
    finally:
        db.close()

def run_schedule():
    """
    Run the scheduler in a separate thread.
    """
    while True:
        schedule.run_pending()
        time.sleep(60)

@app.on_event("startup")
async def startup_event():
    """
    Initialize the application on startup.
    """
    # Schedule news fetching every 3 hours
    schedule.every(3).hours.do(lambda: asyncio.run(fetch_news()))
    
    # Start the scheduler in a separate thread
    scheduler_thread = threading.Thread(target=run_schedule)
    scheduler_thread.daemon = True
    scheduler_thread.start()

@app.get("/")
def read_root():
    """
    Root endpoint.
    """
    return {
        "message": "Welcome to the News Aggregation API",
        "version": settings.VERSION,
        "docs_url": "/docs"
    } 