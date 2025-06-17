from sqlalchemy.orm import Session
from app.repositories.article_repository import ArticleRepository
from app.repositories.external_server_repository import ExternalServerRepository
from app.schemas.article import ArticleCreate
import requests

class NewsService:
    def __init__(self, db: Session):
        self.article_repo = ArticleRepository(db)
        self.server_repo = ExternalServerRepository(db)

    def fetch_and_store_news(self, server_id: int, api_url: str, headers=None, params=None):
        response = requests.get(api_url, headers=headers, params=params)
        if response.status_code == 200:
            news_data = response.json()
            # This part should be customized based on the external API's response structure
            for item in news_data.get('articles', []):
                article = ArticleCreate(
                    title=item.get('title'),
                    description=item.get('description'),
                    content=item.get('content'),
                    source=item.get('source', {}).get('name'),
                    url=item.get('url'),
                    published_at=item.get('publishedAt'),
                    server_id=server_id
                )
                self.article_repo.create(article)
        else:
            raise Exception(f"Failed to fetch news: {response.status_code}") 