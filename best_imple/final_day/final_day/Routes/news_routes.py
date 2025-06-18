from fastapi import APIRouter, HTTPException, Depends, Query
from schemas.news import NewsSearchRequest, NewsArticleResponse
from controllers.news_controller import NewsController
from Utils.jwt_handler import get_current_user
from typing import List, Optional
from datetime import datetime

router = APIRouter(prefix="/news", tags=["news"])

@router.get("/", response_model=List[NewsArticleResponse])
def get_all_news(
    limit: int = Query(10, ge=1, le=100),
    current_user=Depends(get_current_user)
):
    """Get all news articles"""
    try:
        controller = NewsController()
        return controller.get_all_articles(limit)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/today", response_model=List[NewsArticleResponse])
def get_today_news(current_user=Depends(get_current_user)):
    """Get today's news articles"""
    try:
        controller = NewsController()
        return controller.get_today_articles()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/category/{category_name}", response_model=List[NewsArticleResponse])
def get_news_by_category(
    category_name: str,
    limit: int = Query(50, ge=1, le=100),
    current_user=Depends(get_current_user)
):
    """Get news articles by category"""
    try:
        controller = NewsController()
        return controller.get_articles_by_category(category_name, limit)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/search", response_model=List[NewsArticleResponse])
def search_news(
    query: str = Query(..., min_length=1),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    category: Optional[str] = None,
    sort_by: str = Query("published_at", regex="^(published_at|likes|dislikes)$"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    current_user=Depends(get_current_user)
):
    """Search news articles"""
    try:
        controller = NewsController()
        return controller.search_articles(
            query, start_date, end_date, category, sort_by, page, page_size
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{article_id}", response_model=NewsArticleResponse)
def get_article_by_id(
    article_id: int,
    current_user=Depends(get_current_user)
):
    """Get specific article by ID"""
    try:
        controller = NewsController()
        return controller.get_article_by_id(article_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{article_id}/save")
def save_article(
    article_id: int,
    current_user=Depends(get_current_user)
):
    """Save an article for the current user"""
    try:
        controller = NewsController()
        return controller.save_article(article_id, current_user["user_id"])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{article_id}/unsave")
def unsave_article(
    article_id: int,
    current_user=Depends(get_current_user)
):
    """Remove a saved article for the current user"""
    try:
        controller = NewsController()
        return controller.unsave_article(article_id, current_user["user_id"])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/saved/list", response_model=List[NewsArticleResponse])
def get_saved_articles(current_user=Depends(get_current_user)):
    """Get all saved articles for the current user"""
    try:
        controller = NewsController()
        return controller.get_saved_articles(current_user["user_id"])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{article_id}/like")
def like_article(
    article_id: int,
    current_user=Depends(get_current_user)
):
    """Like an article"""
    try:
        controller = NewsController()
        return controller.like_article(article_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{article_id}/dislike")
def dislike_article(
    article_id: int,
    current_user=Depends(get_current_user)
):
    """Dislike an article"""
    try:
        controller = NewsController()
        return controller.dislike_article(article_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))