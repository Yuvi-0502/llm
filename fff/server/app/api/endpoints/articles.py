from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from ...db.session import get_db
from ...models.user import User
from ...models.article import Article, ArticleCategory
from ...schemas.article import Article as ArticleSchema, ArticleSearchParams
from ..deps import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[ArticleSchema])
async def read_articles(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    category: ArticleCategory = None,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    query = db.query(Article)
    if category:
        query = query.filter(Article.category == category)
    articles = query.order_by(Article.published_at.desc()).offset(skip).limit(limit).all()
    return articles

@router.get("/today", response_model=List[ArticleSchema])
async def read_today_articles(
    db: Session = Depends(get_db),
    category: ArticleCategory = None,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    today = datetime.utcnow().date()
    query = db.query(Article).filter(
        Article.published_at >= today,
        Article.published_at < today + timedelta(days=1)
    )
    if category:
        query = query.filter(Article.category == category)
    articles = query.order_by(Article.published_at.desc()).all()
    return articles

@router.get("/date-range", response_model=List[ArticleSchema])
async def read_articles_by_date_range(
    db: Session = Depends(get_db),
    start_date: datetime = None,
    end_date: datetime = None,
    category: ArticleCategory = None,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    query = db.query(Article)
    if start_date and end_date:
        query = query.filter(Article.published_at.between(start_date, end_date))
    if category:
        query = query.filter(Article.category == category)
    articles = query.order_by(Article.published_at.desc()).all()
    return articles

@router.post("/search", response_model=List[ArticleSchema])
async def search_articles(
    *,
    db: Session = Depends(get_db),
    search_params: ArticleSearchParams,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    query = db.query(Article).filter(
        Article.title.ilike(f"%{search_params.query}%") |
        Article.description.ilike(f"%{search_params.query}%")
    )
    
    if search_params.start_date and search_params.end_date:
        query = query.filter(
            Article.published_at.between(search_params.start_date, search_params.end_date)
        )
    
    if search_params.category:
        query = query.filter(Article.category == search_params.category)
    
    # Apply sorting
    if search_params.sort_by == "likes":
        query = query.order_by(Article.likes.desc() if search_params.sort_order == "desc" else Article.likes.asc())
    elif search_params.sort_by == "dislikes":
        query = query.order_by(Article.dislikes.desc() if search_params.sort_order == "desc" else Article.dislikes.asc())
    else:
        query = query.order_by(Article.published_at.desc() if search_params.sort_order == "desc" else Article.published_at.asc())
    
    articles = query.all()
    return articles

@router.post("/{article_id}/save")
async def save_article(
    *,
    db: Session = Depends(get_db),
    article_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    if article not in current_user.saved_articles:
        current_user.saved_articles.append(article)
        db.commit()
    
    return {"message": "Article saved successfully"}

@router.delete("/{article_id}/save")
async def unsave_article(
    *,
    db: Session = Depends(get_db),
    article_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    if article in current_user.saved_articles:
        current_user.saved_articles.remove(article)
        db.commit()
    
    return {"message": "Article unsaved successfully"}

@router.get("/saved", response_model=List[ArticleSchema])
async def read_saved_articles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    return current_user.saved_articles

@router.post("/{article_id}/like")
async def like_article(
    *,
    db: Session = Depends(get_db),
    article_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    article.likes += 1
    db.commit()
    return {"message": "Article liked successfully"}

@router.post("/{article_id}/dislike")
async def dislike_article(
    *,
    db: Session = Depends(get_db),
    article_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    article.dislikes += 1
    db.commit()
    return {"message": "Article disliked successfully"} 