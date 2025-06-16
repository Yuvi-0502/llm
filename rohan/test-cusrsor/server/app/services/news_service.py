import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any
import aiohttp
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.models import Article, Category, ExternalServer
from app.services.category_service import categorize_article

settings = get_settings()


async def fetch_news_api(session: aiohttp.ClientSession, api_key: str) -> List[Dict[str, Any]]:
    """Fetch news from NewsAPI"""
    url = f"https://newsapi.org/v2/top-headlines"
    params = {
        "country": "us",
        "apiKey": api_key
    }
    
    async with session.get(url, params=params) as response:
        if response.status == 200:
            data = await response.json()
            return data.get("articles", [])
        return []


async def fetch_the_news_api(session: aiohttp.ClientSession, api_key: str) -> List[Dict[str, Any]]:
    """Fetch news from The News API"""
    url = f"https://api.thenewsapi.com/v1/news/top"
    params = {
        "api_token": api_key,
        "locale": "us",
        "limit": 10
    }
    
    async with session.get(url, params=params) as response:
        if response.status == 200:
            data = await response.json()
            return data.get("data", [])
        return []


async def fetch_firebase_api(session: aiohttp.ClientSession) -> List[Dict[str, Any]]:
    """Fetch news from Firebase API"""
    url = "https://us-central1-symbolic-gift-98004.cloudfunctions.net/newsapi"
    params = {
        "country": "us",
        "category": "business"
    }
    headers = {
        "api-key": settings.FIREBASE_API_KEY
    }
    
    async with session.get(url, params=params, headers=headers) as response:
        if response.status == 200:
            data = await response.json()
            return data.get("articles", [])
        return []


def process_news_api_article(article: Dict[str, Any]) -> Dict[str, Any]:
    """Process article from NewsAPI format"""
    return {
        "title": article.get("title", ""),
        "description": article.get("description", ""),
        "content": article.get("content", ""),
        "url": article.get("url", ""),
        "source": article.get("source", {}).get("name", ""),
        "published_at": datetime.fromisoformat(article.get("publishedAt", "").replace("Z", "+00:00")),
    }


def process_the_news_api_article(article: Dict[str, Any]) -> Dict[str, Any]:
    """Process article from The News API format"""
    return {
        "title": article.get("title", ""),
        "description": article.get("description", ""),
        "content": article.get("content", ""),
        "url": article.get("url", ""),
        "source": article.get("source", ""),
        "published_at": datetime.fromisoformat(article.get("published_at", "").replace("Z", "+00:00")),
    }


async def fetch_all_news(db: Session) -> None:
    """Fetch news from all configured external APIs"""
    async with aiohttp.ClientSession() as session:
        # Get all active external servers
        external_servers = db.query(ExternalServer).filter(ExternalServer.is_active == True).all()
        
        for server in external_servers:
            try:
                if "newsapi.org" in server.base_url:
                    articles = await fetch_news_api(session, server.api_key)
                    process_func = process_news_api_article
                elif "thenewsapi.com" in server.base_url:
                    articles = await fetch_the_news_api(session, server.api_key)
                    process_func = process_the_news_api_article
                else:
                    continue

                for article_data in articles:
                    processed_article = process_func(article_data)
                    
                    # Check if article already exists
                    existing_article = db.query(Article).filter(
                        Article.url == processed_article["url"]
                    ).first()
                    
                    if not existing_article:
                        # Create new article
                        article = Article(**processed_article)
                        
                        # Categorize article if no category is provided
                        if not article.category_id:
                            category = await categorize_article(article.title + " " + article.description)
                            if category:
                                article.category_id = category.id
                        
                        db.add(article)
                
                # Update last accessed time
                server.last_accessed = datetime.utcnow()
                db.commit()
                
            except Exception as e:
                print(f"Error fetching news from {server.name}: {str(e)}")
                continue


def start_news_fetcher(db: Session) -> None:
    """Start the news fetcher in the background"""
    asyncio.create_task(fetch_all_news(db)) 