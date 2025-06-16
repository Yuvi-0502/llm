from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.api import deps
from app.models.models import Article, User
from app.schemas.article import ArticleResponse, ArticleCreate
from app.services.news_service import fetch_all_news

router = APIRouter()


@router.get("/headlines", response_model=List[ArticleResponse])
def get_headlines(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    category: Optional[str] = None,
) -> Any:
    """
    Get news headlines, optionally filtered by category.
    """
    query = db.query(Article)
    
    if category:
        query = query.filter(Article.category.has(name=category))
    
    # Get articles from the last 24 hours
    yesterday = datetime.utcnow() - timedelta(days=1)
    query = query.filter(Article.published_at >= yesterday)
    
    articles = query.order_by(Article.published_at.desc()).all()
    return articles


@router.get("/saved", response_model=List[ArticleResponse])
def get_saved_articles(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get user's saved articles.
    """
    return current_user.saved_articles


@router.post("/{article_id}/save", response_model=ArticleResponse)
def save_article(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    article_id: int,
) -> Any:
    """
    Save an article for the current user.
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    if article in current_user.saved_articles:
        raise HTTPException(status_code=400, detail="Article already saved")
    
    current_user.saved_articles.append(article)
    db.commit()
    db.refresh(article)
    return article


@router.delete("/{article_id}/save", response_model=ArticleResponse)
def delete_saved_article(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    article_id: int,
) -> Any:
    """
    Delete a saved article for the current user.
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    if article not in current_user.saved_articles:
        raise HTTPException(status_code=400, detail="Article not saved")
    
    current_user.saved_articles.remove(article)
    db.commit()
    db.refresh(article)
    return article


@router.get("/search", response_model=List[ArticleResponse])
def search_articles(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    query: str = Query(..., min_length=1),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> Any:
    """
    Search articles by query and optional date range.
    """
    search_query = db.query(Article).filter(
        Article.title.ilike(f"%{query}%") | Article.description.ilike(f"%{query}%")
    )
    
    if start_date:
        search_query = search_query.filter(Article.published_at >= start_date)
    if end_date:
        search_query = search_query.filter(Article.published_at <= end_date)
    
    articles = search_query.order_by(Article.published_at.desc()).all()
    return articles


@router.post("/refresh", response_model=List[ArticleResponse])
def refresh_articles(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Manually trigger news refresh (admin only).
    """
    fetch_all_news(db)
    return db.query(Article).order_by(Article.published_at.desc()).limit(10).all() 