import schedule
import time
import asyncio
from threading import Thread
from sqlalchemy.orm import Session
from ..db.session import SessionLocal
from ..services.news import NewsService
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.services.article import ArticleService

def run_async_news_fetch():
    async def fetch_news():
        db = SessionLocal()
        try:
            news_service = NewsService(db)
            await news_service.fetch_all_news()
        finally:
            db.close()

    asyncio.run(fetch_news())

def run_scheduler():
    # Schedule news fetching every 3 hours
    schedule.every(3).hours.do(run_async_news_fetch)
    
    # Run immediately on startup
    run_async_news_fetch()
    
    while True:
        schedule.run_pending()
        time.sleep(60)

def start_scheduler():
    scheduler_thread = Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

def fetch_news(article_service: ArticleService):
    """Fetch news from external APIs."""
    try:
        # Get active external APIs
        apis = article_service.get_active_apis()
        
        for api in apis:
            try:
                # Fetch articles from each API
                articles = article_service.fetch_articles_from_api(api)
                
                # Process and save articles
                for article in articles:
                    article_service.create_article(article)
                    
                # Update last accessed timestamp
                article_service.update_last_accessed(api.id)
                
            except Exception as e:
                print(f"Error fetching from API {api.name}: {str(e)}")
                
    except Exception as e:
        print(f"Error in news fetching job: {str(e)}")

def start_scheduler(article_service: ArticleService):
    """Start the news fetching scheduler."""
    scheduler = BackgroundScheduler()
    
    # Schedule news fetching every hour
    scheduler.add_job(
        fetch_news,
        CronTrigger(hour='*'),  # Run every hour
        args=[article_service],
        id='fetch_news',
        replace_existing=True
    )
    
    scheduler.start() 