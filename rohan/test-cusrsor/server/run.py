import uvicorn
from app.core.config import get_settings
from app.db.session import SessionLocal
from app.services.news_service import start_news_fetcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

settings = get_settings()


def start_news_scheduler():
    """Start the news fetcher scheduler"""
    scheduler = AsyncIOScheduler()
    
    # Schedule news fetching every 3 hours
    scheduler.add_job(
        start_news_fetcher,
        trigger=IntervalTrigger(hours=3),
        args=[SessionLocal()],
        id='fetch_news',
        name='Fetch news from external APIs',
        replace_existing=True
    )
    
    scheduler.start()


if __name__ == "__main__":
    # Start the news scheduler
    start_news_scheduler()
    
    # Start the FastAPI application
    uvicorn.run(
        "app.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG,
        reload_dirs=["app"] if settings.DEBUG else None,
        log_level="debug" if settings.DEBUG else "info",
        workers=settings.WORKERS_COUNT if not settings.DEBUG else 1
    ) 