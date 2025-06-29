from fastapi import APIRouter, Depends, Query, Path
from typing import Optional

from server.controller.user_controller import UserController
from server.core.jwt_utils import get_current_user

router = APIRouter(prefix="/user", tags=["user"])
controller = UserController()

@router.get("/headlines/today")
def get_today_headlines(
    category: Optional[str] = Query(None, description="Filter by category"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=100, description="Number of articles per page")
):
    """Get today's headlines with optional category filter and pagination"""
    return controller.get_today_headlines(category, page, limit)

@router.get("/headlines/date-range")
def get_headlines_by_date_range(
    start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(..., description="End date (YYYY-MM-DD)"),
    category: Optional[str] = Query(None, description="Filter by category"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=100, description="Number of articles per page")
):
    """Get headlines for a date range with optional category filter and pagination"""
    return controller.get_headlines_by_date_range(start_date, end_date, category, page, limit)

@router.get("/articles/{article_id}")
def get_article_by_id(
    article_id: int = Path(..., description="Article ID")
):
    """Get a specific article by ID"""
    return controller.get_article_by_id(article_id)

@router.get("/categories")
def get_categories():
    """Get all available categories"""
    return controller.get_categories()

@router.get("/categories/{category}/articles")
def get_articles_by_category(
    category: str = Path(..., description="Category name"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=100, description="Number of articles per page")
):
    """Get articles by specific category with pagination"""
    return controller.get_articles_by_category(category, page, limit)

@router.get("/saved-articles")
def get_saved_articles(
    user=Depends(get_current_user),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=100, description="Number of articles per page")
):
    """Get saved articles for the current user with pagination"""
    return controller.get_saved_articles(user['user_id'], page, limit)

@router.post("/saved-articles")
def save_article(
    article_id: int = Query(..., description="Article ID to save"),
    user=Depends(get_current_user)
):
    """Save an article for the current user"""
    return controller.save_article(user['user_id'], article_id)

@router.delete("/saved-articles/{article_id}")
def delete_saved_article(
    article_id: int = Path(..., description="Article ID to remove"),
    user=Depends(get_current_user)
):
    """Delete a saved article for the current user"""
    return controller.delete_article(user['user_id'], article_id)

@router.get("/search")
def search_articles(
    query: str = Query(..., description="Search query"),
    start_date: Optional[str] = Query(None, description="Start date filter (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date filter (YYYY-MM-DD)"),
    sort_by: str = Query("published_at", description="Sort by: likes, dislikes, or published_at"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=100, description="Number of articles per page")
):
    """Search articles with advanced filtering and sorting"""
    return controller.search_articles(query, start_date, end_date, sort_by, page, limit)

@router.get("/notifications")
def get_notifications(
    user=Depends(get_current_user),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=100, description="Number of notifications per page")
):
    """Get notifications for the current user with pagination"""
    return controller.get_notifications(user['user_id'], page, limit)

@router.post("/logout")
def logout(user=Depends(get_current_user)):
    """Logout the current user"""
    return controller.logout(user['user_id'])

