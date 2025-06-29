from fastapi import APIRouter, Query
from server.controller.news_controller-1 import NewsController
from typing import Optional

router = APIRouter(prefix="/news", tags=["news"])
controller = NewsController()

@router.post("/fetch")
def fetch_news_manual():
    """Manually trigger news fetching from external APIs"""
    return controller.fetch_news()

@router.get("/status")
def get_news_status():
    """Get status of news fetching and database"""
    return controller.get_news_status()

@router.get("/articles")
def get_all_articles(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=100, description="Number of articles per page"),
    category: Optional[str] = Query(None, description="Filter by category"),
    sort_by: str = Query("published_at", description="Sort by: likes, dislikes, or published_at")
):
    """Get all articles with pagination, filtering, and sorting"""
    return controller.get_all_articles(page, limit, category, sort_by)

@router.get("/articles/{article_id}")
def get_article_by_id(article_id: int):
    """Get a specific article by ID"""
    return controller.get_article_by_id(article_id)

@router.get("/categories")
def get_categories():
    """Get all available categories"""
    return controller.get_categories()

@router.get("/categories/{category}/articles")
def get_articles_by_category(
    category: str,
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=100, description="Number of articles per page")
):
    """Get articles by specific category"""
    return controller.get_articles_by_category(category, page, limit)

@router.get("/search")
def search_articles(
    query: str = Query(..., description="Search query"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=100, description="Number of articles per page"),
    category: Optional[str] = Query(None, description="Filter by category"),
    sort_by: str = Query("published_at", description="Sort by: likes, dislikes, or published_at")
):
    """Search articles with advanced filtering"""
    return controller.search_articles(query, page, limit, category, sort_by)

@router.get("/today")
def get_today_articles(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=100, description="Number of articles per page"),
    category: Optional[str] = Query(None, description="Filter by category")
):
    """Get today's articles with pagination and category filter"""
    return controller.get_today_articles(page, limit, category)

@router.get("/date-range")
def get_articles_by_date_range(
    start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(..., description="End date (YYYY-MM-DD)"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=100, description="Number of articles per page"),
    category: Optional[str] = Query(None, description="Filter by category")
):
    """Get articles for a date range with pagination and category filter"""
    return controller.get_articles_by_date_range(start_date, end_date, page, limit, category)

