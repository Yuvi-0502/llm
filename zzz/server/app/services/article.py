from typing import List, Optional, Tuple
from datetime import datetime
from app.models.article import Article, ArticleCategory
from app.schemas.article import ArticleCreate, ArticleUpdate
from app.repositories.article_repository import ArticleRepository
from .categorization import ArticleCategorizer

class ArticleService:
    """Service for article business logic."""
    
    def __init__(self, repository: ArticleRepository, categorizer: ArticleCategorizer):
        self.repository = repository
        self.categorizer = categorizer

    def get_articles(
        self,
        skip: int = 0,
        limit: int = 100,
        category: Optional[ArticleCategory] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        min_confidence: float = 0.0
    ) -> List[Article]:
        articles = self.repository.get_all(
            skip=skip,
            limit=limit,
            category=category,
            start_date=start_date,
            end_date=end_date
        )
        
        if min_confidence > 0:
            return [
                article for article in articles
                if article.category_confidence >= min_confidence
            ]
            
        return articles

    def get_article(self, article_id: int) -> Optional[Article]:
        return self.repository.get(article_id)

    def create_article(self, article: ArticleCreate) -> Article:
        # If no category is provided, try to categorize the article
        if not article.category:
            category, confidence = self.categorizer.get_category_confidence(
                article.title,
                article.description,
                article.content
            )
            article.category = category
            article.category_confidence = confidence
        else:
            # If category is provided, calculate confidence anyway
            _, confidence = self.categorizer.get_category_confidence(
                article.title,
                article.description,
                article.content
            )
            article.category_confidence = confidence
            
        db_article = Article(**article.dict())
        return self.repository.create(db_article)

    def update_article(self, article_id: int, article: ArticleUpdate) -> Optional[Article]:
        db_article = self.repository.get(article_id)
        if not db_article:
            return None
            
        update_data = article.dict(exclude_unset=True)
        
        # If category is being updated to None, try to recategorize
        if "category" in update_data and update_data["category"] is None:
            category, confidence = self.categorizer.get_category_confidence(
                db_article.title,
                db_article.description,
                db_article.content
            )
            update_data["category"] = category
            update_data["category_confidence"] = confidence
        elif "category" in update_data:
            # If category is being changed, recalculate confidence
            _, confidence = self.categorizer.get_category_confidence(
                db_article.title,
                db_article.description,
                db_article.content
            )
            update_data["category_confidence"] = confidence
            
        for key, value in update_data.items():
            setattr(db_article, key, value)
            
        return self.repository.update(article_id, db_article)

    def delete_article(self, article_id: int) -> bool:
        return self.repository.delete(article_id)

    def get_today_articles(self, min_confidence: float = 0.0) -> List[Article]:
        articles = self.repository.get_today_articles()
        
        if min_confidence > 0:
            return [
                article for article in articles
                if article.category_confidence >= min_confidence
            ]
            
        return articles

    def search_articles(
        self,
        query: str,
        category: Optional[ArticleCategory] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        min_confidence: float = 0.0
    ) -> List[Article]:
        articles = self.repository.search_articles(
            query=query,
            category=category,
            start_date=start_date,
            end_date=end_date
        )
        
        if min_confidence > 0:
            return [
                article for article in articles
                if article.category_confidence >= min_confidence
            ]
            
        return articles

    def get_articles_by_confidence(
        self,
        category: Optional[ArticleCategory] = None,
        min_confidence: float = 0.0,
        max_confidence: float = 1.0
    ) -> List[Article]:
        """Get articles filtered by category confidence scores."""
        articles = self.repository.get_all(category=category)
        return [
            article for article in articles
            if min_confidence <= article.category_confidence <= max_confidence
        ] 