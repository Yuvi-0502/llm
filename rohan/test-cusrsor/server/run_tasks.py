import asyncio
import logging
from app.core.config import get_settings
from app.services.article_service import ArticleService
from app.services.notification_service import NotificationService
from app.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()


async def run_tasks():
    db = SessionLocal()
    try:
        article_service = ArticleService(db)
        notification_service = NotificationService(db)

        while True:
            try:
                # Fetch and store articles
                await article_service.fetch_and_store_articles()
                
                # Send notifications
                await notification_service.send_notifications()
                
                # Wait for the next iteration
                await asyncio.sleep(settings.TASK_INTERVAL)
            except Exception as e:
                logger.error(f"Error in background tasks: {e}")
                await asyncio.sleep(60)  # Wait a minute before retrying
    finally:
        db.close()


if __name__ == "__main__":
    logger.info("Starting background tasks")
    asyncio.run(run_tasks()) 