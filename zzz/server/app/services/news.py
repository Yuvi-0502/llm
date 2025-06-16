import aiohttp
import asyncio
from datetime import datetime
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from ..models.article import Article, ArticleCategory
from ..models.external_api import ExternalAPI
from ..core.config import settings
import re
from collections import Counter

class NewsService:
    def __init__(self, db: Session):
        self.db = db
        self.category_keywords = {
            ArticleCategory.BUSINESS: ['business', 'economy', 'market', 'stock', 'finance', 'trade'],
            ArticleCategory.ENTERTAINMENT: ['entertainment', 'movie', 'music', 'celebrity', 'film', 'show'],
            ArticleCategory.SPORTS: ['sport', 'football', 'basketball', 'tennis', 'game', 'match'],
            ArticleCategory.TECHNOLOGY: ['technology', 'tech', 'software', 'hardware', 'digital', 'computer']
        }

    async def fetch_news_api_articles(self, api: ExternalAPI) -> List[Dict]:
        async with aiohttp.ClientSession() as session:
            try:
                url = f"{api.base_url}/top-headlines"
                params = {
                    "country": "us",
                    "apiKey": api.api_key
                }
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("articles", [])
            except Exception as e:
                print(f"Error fetching from News API: {str(e)}")
            return []

    async def fetch_thenews_api_articles(self, api: ExternalAPI) -> List[Dict]:
        async with aiohttp.ClientSession() as session:
            try:
                url = f"{api.base_url}/news/top"
                params = {
                    "api_token": api.api_key,
                    "locale": "us",
                    "limit": 10
                }
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("data", [])
            except Exception as e:
                print(f"Error fetching from The News API: {str(e)}")
            return []

    def detect_category(self, title: str, description: str) -> ArticleCategory:
        text = f"{title} {description}".lower()
        word_counts = Counter(re.findall(r'\w+', text))
        
        category_scores = {
            category: sum(word_counts[word] for word in keywords)
            for category, keywords in self.category_keywords.items()
        }
        
        if not any(category_scores.values()):
            return ArticleCategory.GENERAL
            
        return max(category_scores.items(), key=lambda x: x[1])[0]

    def process_article(self, article_data: Dict, source: str) -> Optional[Article]:
        try:
            title = article_data.get("title", "")
            description = article_data.get("description", "")
            
            if not title:
                return None
                
            category = self.detect_category(title, description)
            
            return Article(
                title=title,
                description=description,
                content=article_data.get("content", ""),
                url=article_data.get("url", ""),
                image_url=article_data.get("urlToImage", ""),
                source_name=article_data.get("source", {}).get("name", source),
                source_id=article_data.get("source", {}).get("id", ""),
                author=article_data.get("author", ""),
                published_at=datetime.fromisoformat(article_data.get("publishedAt", "").replace("Z", "+00:00")),
                category=category
            )
        except Exception as e:
            print(f"Error processing article: {str(e)}")
            return None

    async def fetch_all_news(self):
        apis = self.db.query(ExternalAPI).filter(ExternalAPI.is_active == True).all()
        
        for api in apis:
            if "newsapi.org" in api.base_url:
                articles_data = await self.fetch_news_api_articles(api)
            else:
                articles_data = await self.fetch_thenews_api_articles(api)
            
            for article_data in articles_data:
                article = self.process_article(article_data, api.name)
                if article:
                    existing = self.db.query(Article).filter(
                        Article.title == article.title,
                        Article.source_name == article.source_name
                    ).first()
                    
                    if not existing:
                        self.db.add(article)
            
            api.last_accessed = datetime.utcnow()
            self.db.commit()

    def get_articles_by_category(self, category: ArticleCategory, limit: int = 10) -> List[Article]:
        return self.db.query(Article).filter(
            Article.category == category
        ).order_by(Article.published_at.desc()).limit(limit).all()

    def get_articles_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Article]:
        return self.db.query(Article).filter(
            Article.published_at.between(start_date, end_date)
        ).order_by(Article.published_at.desc()).all()

    def search_articles(self, query: str, start_date: Optional[datetime] = None, 
                       end_date: Optional[datetime] = None) -> List[Article]:
        search_query = self.db.query(Article).filter(
            Article.title.ilike(f"%{query}%") | 
            Article.description.ilike(f"%{query}%")
        )
        
        if start_date and end_date:
            search_query = search_query.filter(
                Article.published_at.between(start_date, end_date)
            )
            
        return search_query.order_by(Article.published_at.desc()).all() 