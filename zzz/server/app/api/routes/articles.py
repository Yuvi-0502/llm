from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.container import Container, get_container
from app.core.security import get_current_user
from app.dto.article import (
    ArticleResponseDTO,
    ArticleCreateDTO,
    ArticleUpdateDTO,
    ArticleSearchDTO,
    ArticleListResponseDTO,
    ArticleCategoryResponseDTO
)
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=ArticleListResponseDTO)
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
    articles = container.article_service.get_articles(
        skip=skip,
        limit=limit,
        category=category,
        start_date=start_date,
        end_date=end_date,
        min_confidence=min_confidence
    )
    total = container.article_service.get_articles_count(
        category=category,
        start_date=start_date,
        end_date=end_date,
        min_confidence=min_confidence
    )
    return ArticleListResponseDTO(
        articles=articles,
        total=total,
        page=skip // limit + 1,
        size=limit
    )

@router.get("/today", response_model=ArticleListResponseDTO)
async def read_today_articles(
    min_confidence: float = 0.0,
    container: Container = Depends(get_container)
):
    """Get today's articles."""
    articles = container.article_service.get_today_articles(
        min_confidence=min_confidence
    )
    total = len(articles)
    return ArticleListResponseDTO(
        articles=articles,
        total=total,
        page=1,
        size=total
    )

@router.get("/search", response_model=ArticleListResponseDTO)
async def search_articles(
    params: ArticleSearchDTO,
    container: Container = Depends(get_container)
):
    """Search articles."""
    articles = container.article_service.search_articles(
        query=params.query,
        category=params.category,
        start_date=params.start_date,
        end_date=params.end_date,
        min_confidence=params.min_confidence
    )
    total = len(articles)
    return ArticleListResponseDTO(
        articles=articles,
        total=total,
        page=1,
        size=total
    )

@router.get("/categories", response_model=List[ArticleCategoryResponseDTO])
async def get_category_stats(
    container: Container = Depends(get_container)
):
    """Get article statistics by category."""
    return container.article_service.get_category_stats()

@router.get("/{article_id}", response_model=ArticleResponseDTO)
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

@router.post("/", response_model=ArticleResponseDTO)
async def create_article(
    article: ArticleCreateDTO,
    current_user: User = Depends(get_current_user),
    container: Container = Depends(get_container)
):
    """Create new article."""
    return container.article_service.create_article(article=article)

@router.put("/{article_id}", response_model=ArticleResponseDTO)
async def update_article(
    article_id: int,
    article: ArticleUpdateDTO,
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