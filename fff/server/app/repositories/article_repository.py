from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.article import Article, ArticleCategory
from .base_repository import BaseRepository

class ArticleRepository(BaseRepository[Article]):
    """Repository for article database operations."""
    
    def get(self, id: int) -> Optional[Article]:
        return self.db.query(Article).filter(Article.id == id).first()
    
    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        category: Optional[ArticleCategory] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Article]:
        query = self.db.query(Article)
        
        if category:
            query = query.filter(Article.category == category)
        if start_date:
            query = query.filter(Article.published_at >= start_date)
        if end_date:
            query = query.filter(Article.published_at <= end_date)
            
        return query.offset(skip).limit(limit).all()
    
    def create(self, article: Article) -> Article:
        self.db.add(article)
        self.db.commit()
        self.db.refresh(article)
        return article
    
    def update(self, id: int, article: Article) -> Optional[Article]:
        db_article = self.get(id)
        if not db_article:
            return None
            
        for key, value in article.__dict__.items():
            if not key.startswith('_'):
                setattr(db_article, key, value)
                
        self.db.commit()
        self.db.refresh(db_article)
        return db_article
    
    def delete(self, id: int) -> bool:
        article = self.get(id)
        if not article:
            return False
            
        self.db.delete(article)
        self.db.commit()
        return True
    
    def get_today_articles(self) -> List[Article]:
        today = datetime.utcnow().date()
        return self.db.query(Article).filter(
            Article.published_at >= today
        ).all()
    
    def search_articles(
        self,
        query: str,
        category: Optional[ArticleCategory] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Article]:
        search_query = self.db.query(Article).filter(
            Article.title.ilike(f"%{query}%") |
            Article.description.ilike(f"%{query}%") |
            Article.content.ilike(f"%{query}%")
        )
        
        if category:
            search_query = search_query.filter(Article.category == category)
        if start_date:
            search_query = search_query.filter(Article.published_at >= start_date)
        if end_date:
            search_query = search_query.filter(Article.published_at <= end_date)
            
        return search_query.all() 