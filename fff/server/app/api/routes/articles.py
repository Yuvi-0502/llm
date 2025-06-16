from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.container import Container, get_container
from app.core.security import get_current_user
from app.schemas.article import Article, ArticleCreate, ArticleUpdate, ArticleSearchParams
from app.schemas.user import User

router = APIRouter()

@router.get("/", response_model=List[Article])
async def read_articles(
    skip: int = 0,
    limit: int = 100,
    category: str = None,
    start_date: str = None,
    end_date: str = None,
    min_confidence: float = 0.0,
    container: Container = Depends(get_container)
):
    """Get all articles."""
    return container.article_service.get_articles(
        skip=skip,
        limit=limit,
        category=category,
        start_date=start_date,
        end_date=end_date,
        min_confidence=min_confidence
    )

@router.get("/today", response_model=List[Article])
async def read_today_articles(
    min_confidence: float = 0.0,
    container: Container = Depends(get_container)
):
    """Get today's articles."""
    return container.article_service.get_today_articles(
        min_confidence=min_confidence
    )

@router.get("/search", response_model=List[Article])
async def search_articles(
    params: ArticleSearchParams,
    container: Container = Depends(get_container)
):
    """Search articles."""
    return container.article_service.search_articles(
        query=params.query,
        category=params.category,
        start_date=params.start_date,
        end_date=params.end_date,
        min_confidence=params.min_confidence
    )

@router.get("/{article_id}", response_model=Article)
async def read_article(
    article_id: int,
    container: Container = Depends(get_container)
):
    """Get article by ID."""
    article = container.article_service.get_article(article_id=article_id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    return article

@router.post("/", response_model=Article)
async def create_article(
    article: ArticleCreate,
    current_user: User = Depends(get_current_user),
    container: Container = Depends(get_container)
):
    """Create new article."""
    return container.article_service.create_article(article=article)

@router.put("/{article_id}", response_model=Article)
async def update_article(
    article_id: int,
    article: ArticleUpdate,
    current_user: User = Depends(get_current_user),
    container: Container = Depends(get_container)
):
    """Update article."""
    updated_article = container.article_service.update_article(
        article_id=article_id,
        article=article
    )
    if not updated_article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    return updated_article

@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(
    article_id: int,
    current_user: User = Depends(get_current_user),
    container: Container = Depends(get_container)
):
    """Delete article."""
    if not container.article_service.delete_article(article_id=article_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        ) 