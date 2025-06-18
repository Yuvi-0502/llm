from apscheduler.schedulers.background import BackgroundScheduler
from Server.Controllers.news_controller import NewsController
from loguru import logger

def sync_news_job():
    logger.info("Scheduled news sync started...")
    controller = NewsController()
    result = controller.fetch_news()
    print("Scheduled News Sync:", result)
    logger.info(f"Scheduled sync result: {result}")

def start_news_sync_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(sync_news_job, 'interval', hours=4)
    scheduler.start()
    print("News sync scheduler started: will run every 4 hours.")
