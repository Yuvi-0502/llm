from typing import List, Optional
from ..models.article import Article
from ..services.api_client import APIClient

class NewsController:
    def __init__(self, api_client: APIClient):
        self.api_client = api_client

    def get_news(self, category: Optional[str] = None) -> List[Article]:
        try:
            response = self.api_client.get_news(category)
            return [Article(**article) for article in response]
        except Exception as e:
            raise Exception("Error loading news")

    def search_news(self, query: str) -> List[Article]:
        try:
            response = self.api_client.search_news(query)
            return [Article(**article) for article in response]
        except Exception as e:
            raise Exception("Error searching news")

    def get_saved_articles(self) -> List[Article]:
        try:
            response = self.api_client.get_saved_articles()
            return [Article(**article) for article in response]
        except Exception as e:
            raise Exception("Error loading saved articles")

    def save_article(self, article_id: int) -> bool:
        try:
            self.api_client.save_article(article_id)
            return True
        except Exception as e:
            raise Exception("Error saving article") 