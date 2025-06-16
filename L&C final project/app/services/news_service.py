import aiohttp
import asyncio
from typing import List, Dict, Any
from datetime import datetime
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from app.core.config import settings
from app.models.news import NewsArticle, NewsCategory
from sqlalchemy.orm import Session

class NewsService:
    def __init__(self, db: Session):
        self.db = db
        self.news_api_url = "https://newsapi.org/v2/top-headlines"
        self.the_news_api_url = "https://api.thenewsapi.com/v1/news/top"
        
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')

    async def fetch_news_api(self) -> List[Dict[str, Any]]:
        async with aiohttp.ClientSession() as session:
            params = {
                "country": "us",
                "apiKey": settings.NEWS_API_KEY
            }
            async with session.get(self.news_api_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("articles", [])
                return []

    async def fetch_the_news_api(self) -> List[Dict[str, Any]]:
        async with aiohttp.ClientSession() as session:
            params = {
                "api_token": settings.THE_NEWS_API_KEY,
                "locale": "us",
                "limit": 10
            }
            async with session.get(self.the_news_api_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("data", [])
                return []

    def categorize_article(self, title: str, description: str) -> NewsCategory:
        # Combine title and description for better categorization
        text = f"{title} {description}"
        tokens = word_tokenize(text.lower())
        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if word not in stop_words]

        # Define category keywords
        category_keywords = {
            NewsCategory.BUSINESS: ['business', 'market', 'stock', 'economy', 'finance', 'trade'],
            NewsCategory.ENTERTAINMENT: ['entertainment', 'movie', 'music', 'celebrity', 'film', 'show'],
            NewsCategory.SPORTS: ['sport', 'football', 'basketball', 'baseball', 'game', 'player'],
            NewsCategory.TECHNOLOGY: ['tech', 'technology', 'software', 'computer', 'digital', 'internet']
        }

        # Count keyword occurrences
        category_scores = {category: 0 for category in NewsCategory}
        for token in tokens:
            for category, keywords in category_keywords.items():
                if token in keywords:
                    category_scores[category] += 1

        # Return category with highest score, or GENERAL if no clear category
        max_category = max(category_scores.items(), key=lambda x: x[1])
        return max_category[0] if max_category[1] > 0 else NewsCategory.GENERAL

    async def process_and_store_news(self):
        # Fetch news from both APIs concurrently
        news_api_results, the_news_api_results = await asyncio.gather(
            self.fetch_news_api(),
            self.fetch_the_news_api()
        )

        # Process NewsAPI results
        for article in news_api_results:
            if not article.get("title"):
                continue

            category = self.categorize_article(
                article.get("title", ""),
                article.get("description", "")
            )

            news_article = NewsArticle(
                title=article["title"],
                description=article.get("description"),
                content=article.get("content"),
                url=article["url"],
                image_url=article.get("urlToImage"),
                source=article["source"]["name"],
                category=category,
                published_at=article["publishedAt"],
                raw_data=article
            )
            self.db.add(news_article)

        # Process The News API results
        for article in the_news_api_results:
            if not article.get("title"):
                continue

            category = self.categorize_article(
                article.get("title", ""),
                article.get("description", "")
            )

            news_article = NewsArticle(
                title=article["title"],
                description=article.get("description"),
                content=article.get("content"),
                url=article["url"],
                image_url=article.get("image_url"),
                source=article.get("source", "Unknown"),
                category=category,
                published_at=article.get("published_at", datetime.utcnow().isoformat()),
                raw_data=article
            )
            self.db.add(news_article)

        self.db.commit()

    def get_news_by_category(self, category: NewsCategory, page: int = 1, size: int = 10):
        return self.db.query(NewsArticle)\
            .filter(NewsArticle.category == category)\
            .order_by(NewsArticle.published_at.desc())\
            .offset((page - 1) * size)\
            .limit(size)\
            .all()

    def search_news(self, query: str, category: NewsCategory = None, 
                   start_date: datetime = None, end_date: datetime = None,
                   sort_by: str = None, page: int = 1, size: int = 10):
        news_query = self.db.query(NewsArticle)

        if query:
            news_query = news_query.filter(
                NewsArticle.title.ilike(f"%{query}%") |
                NewsArticle.description.ilike(f"%{query}%")
            )

        if category:
            news_query = news_query.filter(NewsArticle.category == category)

        if start_date:
            news_query = news_query.filter(NewsArticle.published_at >= start_date)

        if end_date:
            news_query = news_query.filter(NewsArticle.published_at <= end_date)

        if sort_by == "likes":
            news_query = news_query.order_by(NewsArticle.likes.desc())
        elif sort_by == "dislikes":
            news_query = news_query.order_by(NewsArticle.dislikes.desc())
        else:
            news_query = news_query.order_by(NewsArticle.published_at.desc())

        total = news_query.count()
        articles = news_query.offset((page - 1) * size).limit(size).all()

        return {
            "articles": articles,
            "total": total,
            "page": page,
            "size": size
        } 