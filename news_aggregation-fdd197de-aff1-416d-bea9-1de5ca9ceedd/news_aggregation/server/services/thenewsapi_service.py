# thenewsapi_service.py
import requests
from server.schemas.news-1 import NewsArticleCreate
from server.services.interfaces.external_api_service import ExternalAPIService

class TheNewsAPIService(ExternalAPIService):
    def fetch_news_articles(self, server_config: dict):
        url = server_config["api_url"] + server_config["api_key"]
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                articles = data.get("data", [])
                return [
                    NewsArticleCreate(
                        title=a.get("title"),
                        server_id=server_config["server_id"],
                        description=a.get("description"),
                        content=a.get("content"),
                        source=a.get("source"),
                        url=a.get("url"),
                        published_at=a.get("published_at"),
                        categories=a.get("categories", [])
                    )
                    for a in articles
                ]
        except requests.RequestException as e:
            print(f"[TheNewsAPIService] Error fetching news: {e}")
        return []
