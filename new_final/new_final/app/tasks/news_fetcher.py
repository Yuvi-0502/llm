import threading
import time
from app.services.news_service import NewsService
from app.core.database import SessionLocal

def fetch_news_periodically(interval_hours=3):
    while True:
        db = SessionLocal()
        try:
            news_service = NewsService(db)
            # Example: fetch from all servers (you'd want to loop through servers in DB)
            # news_service.fetch_and_store_news(server_id, api_url, headers, params)
            print("Fetching news...")
        finally:
            db.close()
        time.sleep(interval_hours * 3600)

def start_news_fetcher():
    thread = threading.Thread(target=fetch_news_periodically, daemon=True)
    thread.start() 