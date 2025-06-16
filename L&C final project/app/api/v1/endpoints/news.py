from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Any, List, Optional
from datetime import datetime

from app.api.v1.endpoints.auth import get_current_active_user
from app.db.session import get_db
from app.models.user import User, UserRole
from app.models.news import NewsArticle, NewsCategory
from app.schemas.news import NewsArticle as NewsArticleSchema, NewsArticleList, NewsSearchParams
from app.services.news_service import NewsService

router = APIRouter()

@router.get("/headlines", response_model=NewsArticleList)
def get_headlines(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    category: Optional[NewsCategory] = None,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
) -> Any:
    """
    Get news headlines, optionally filtered by category.
    """
    news_service = NewsService(db)
    if category:
        articles = news_service.get_news_by_category(category, page, size)
        total = db.query(NewsArticle).filter(NewsArticle.category == category).count()
    else:
        articles = db.query(NewsArticle)\
            .order_by(NewsArticle.published_at.desc())\
            .offset((page - 1) * size)\
            .limit(size)\
            .all()
        total = db.query(NewsArticle).count()
    
    return {
        "articles": articles,
        "total": total,
        "page": page,
        "size": size
    }

@router.get("/search", response_model=NewsArticleList)
def search_news(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    query: str,
    category: Optional[NewsCategory] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    sort_by: Optional[str] = None,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
) -> Any:
    """
    Search news articles with various filters.
    """
    news_service = NewsService(db)
    return news_service.search_news(
        query=query,
        category=category,
        start_date=start_date,
        end_date=end_date,
        sort_by=sort_by,
        page=page,
        size=size
    )

@router.post("/articles/{article_id}/save")
def save_article(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    article_id: int,
) -> Any:
    """
    Save an article for the current user.
    """
    article = db.query(NewsArticle).filter(NewsArticle.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )
    
    if article in current_user.saved_articles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Article already saved",
        )
    
    current_user.saved_articles.append(article)
    db.commit()
    return {"message": "Article saved successfully"}

@router.delete("/articles/{article_id}/save")
def unsave_article(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    article_id: int,
) -> Any:
    """
    Remove a saved article for the current user.
    """
    article = db.query(NewsArticle).filter(NewsArticle.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )
    
    if article not in current_user.saved_articles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Article not saved",
        )
    
    current_user.saved_articles.remove(article)
    db.commit()
    return {"message": "Article removed from saved articles"}

@router.get("/saved", response_model=List[NewsArticleSchema])
def get_saved_articles(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get all saved articles for the current user.
    """
    return current_user.saved_articles

@router.post("/articles/{article_id}/like")
def like_article(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    article_id: int,
) -> Any:
    """
    Like an article.
    """
    article = db.query(NewsArticle).filter(NewsArticle.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )
    
    article.likes += 1
    db.commit()
    return {"message": "Article liked successfully"}

@router.post("/articles/{article_id}/dislike")
def dislike_article(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    article_id: int,
) -> Any:
    """
    Dislike an article.
    """
    article = db.query(NewsArticle).filter(NewsArticle.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )
    
    article.dislikes += 1
    db.commit()
    return {"message": "Article disliked successfully"} 